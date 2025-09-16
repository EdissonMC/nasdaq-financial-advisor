from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.analysis import analyze_text
from app import models, schemas, database

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

@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze(input: InputText, db: Session = Depends(get_db)):
    # Run analysis
    result = analyze_text(input.text)

    # Create DB record
    db_entry = models.Analysis(
        text=input.text,
        sentiment_pos=result["sentiment"]["pos"],
        sentiment_neg=result["sentiment"]["neg"],
        sentiment_neu=result["sentiment"]["neu"],
        sentiment_compound=result["sentiment"]["compound"],
        polarity=result["blob_polarity"]["polarity"],
        subjectivity=result["blob_polarity"]["subjectivity"],
    )

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry

@app.get("/analyses", response_model=list[schemas.AnalysisResponse])
def get_analyses(db: Session = Depends(get_db)):
    """Retrieve all past analyses"""
    return db.query(models.Analysis).all()
