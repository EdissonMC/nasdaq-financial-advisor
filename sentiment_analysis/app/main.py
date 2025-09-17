from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.analysis import analyze_text
from app import models, schemas, database

from openai import OpenAI
import os


# Initialize OpenAI client once
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency: get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InputText(BaseModel):
    text: str
    explain_with_llm: bool = False  # optional flag

@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze(input: InputText, db: Session = Depends(get_db)):
    # Run analysis (now passing explain_with_llm)
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
    api_response = schemas.AnalysisResponse.from_orm(db_entry)
    if explanation:
        api_response.llm_explanation = explanation

    return api_response
    

@app.get("/analyses", response_model=list[schemas.AnalysisResponse])
def get_analyses(db: Session = Depends(get_db)):
    """Retrieve all past analyses"""
    return db.query(models.Analysis).all()
