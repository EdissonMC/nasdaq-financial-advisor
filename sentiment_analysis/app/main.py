from fastapi import FastAPI, Depends , HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from pydantic import BaseModel

from openai import OpenAI
import os
import logging

# MODIFY EXISTING IMPORTS
from . import models, schemas  # Add dot for relative imports
from .database import engine, get_db, create_tables  # Use database.py functions
from .analysis import analyze_text  # Use class instead of function

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize OpenAI client once
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create DB tables
try:
    create_tables()  # Use function from database.py
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

app = FastAPI(
    title="Sentiment Analysis API",
    description="Financial sentiment analysis microservice",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Events on application startup"""
    logger.info("Sentiment Analysis API started")
   

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Sentiment Analysis API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "sentiment-analysis",
        "database": "connected",
        "nlp_models": "loaded"
    }
class InputText(BaseModel):
    text: str
    explain_with_llm: bool = False
    user_id: int | None = None
@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze_sentiment(input: InputText, db: Session = Depends(get_db)):
    try:
        result = analyze_text(input.text, explain_with_llm=input.explain_with_llm)

        # Create DB record
        db_entry = models.Analysis(
            text=input.text,
            sentiment_pos=result["sentiment"]["pos"],
            sentiment_neg=result["sentiment"]["neg"],
            sentiment_neu=result["sentiment"]["neu"],
            sentiment_compound=result["sentiment"]["compound"],
            polarity=result["blob_polarity"]["polarity"],
            subjectivity=result["blob_polarity"]["subjectivity"],
            llm_explanation=result.get("llm_explanation"),  # ✅ save if exists
            user_id=input.user_id
        )

        # Optional LLM explanation
        explanation = None
        if input.explain_with_llm:
            prompt = f"""
            Analyze the following text for sentiment and subjectivity:

            Text: "{input.text}"

            Sentiment scores:
            - Positive: {result['sentiment']['pos']}
            - Negative: {result['sentiment']['neg']}
            - Neutral: {result['sentiment']['neu']}
            - Compound: {result['sentiment']['compound']}

            Polarity: {result['blob_polarity']['polarity']}
            Subjectivity: {result['blob_polarity']['subjectivity']}

            Provide a concise explanation (2-3 sentences) in plain English for a non-technical user.
            """
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful assistant for sentiment analysis."},
                        {"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7,
            )
            explanation = response.choices[0].message.content.strip()
            db_entry.llm_explanation = explanation  # store in DB if column exists

        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)

        # Add explanation to API response dynamically
        api_response = schemas.AnalysisResponse.model_validate(db_entry)
        if explanation:
            api_response.llm_explanation = explanation

        return api_response
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/analyses", response_model=list[schemas.AnalysisResponse])
def get_analyses(
    user_id: int = None,  # ✅ ADD for chat-api compatibility
    limit: int = 50,
    db: Session = Depends(get_db)):
    """Retrieve all past analyses"""
    query = db.query(models.Analysis)
    
    if user_id:
        query = query.filter(models.Analysis.user_id == user_id)
    
    analyses = query.order_by(models.Analysis.created_at.desc()).limit(limit).all()
    return analyses


@app.get("/analyses/{analysis_id}", response_model=schemas.AnalysisResponse)
def get_analysis_by_id(analysis_id: int, db: Session = Depends(get_db)):
    """Get specific analysis by ID"""
    try:
        analysis = db.query(models.Analysis).filter(models.Analysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return analysis
    except Exception as e:
        logger.error(f"Error fetching analysis {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from . import database  # ✅ IMPORTAR EL MÓDULO database
from . import analysis
@app.get("/admin/dashboard", response_model=schemas.AdminDashboardData)
def get_admin_dashboard(db: Session = Depends(database.get_db)):
    dashboard_data = analysis.get_admin_dashboard_data(db)
    if dashboard_data is None:
        raise HTTPException(status_code=404, detail="No analysis records found")
    return dashboard_data

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8001))  # ✅ CHANGE from 8000 to 8001
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
