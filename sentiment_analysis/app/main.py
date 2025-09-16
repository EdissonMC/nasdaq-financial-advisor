from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.analysis import analyze_text
import app.models as models
import app.database as database
import app.schemas as schemas

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


class InputText(BaseModel):
    text: str


# Dependency: get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/analyze", response_model=schemas.AnalysisOut)
def analyze(input: InputText, db: Session = Depends(get_db)):
    # Run analysis
    result = analyze_text(input.text)

    # Save result to DB
    db_entry = models.AnalysisResult(
        text=input.text,
        sentiment=result["sentiment"],
        bow=result["bow"],
        blob_polarity=result["blob_polarity"],
        polarity=result["blob_polarity"]["polarity"],
        subjectivity=result["blob_polarity"]["subjectivity"],
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry

