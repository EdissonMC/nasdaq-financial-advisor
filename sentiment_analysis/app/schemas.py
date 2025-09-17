from pydantic import BaseModel
from datetime import datetime

class AnalysisBase(BaseModel):
    text: str
    sentiment_pos: float
    sentiment_neg: float
    sentiment_neu: float
    sentiment_compound: float
    polarity: float
    subjectivity: float
    created_at: datetime | None = None
    llm_explanation: str | None = None


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisResponse(BaseModel):
    id: int
    text: str
    sentiment_pos: float
    sentiment_neg: float
    sentiment_neu: float
    sentiment_compound: float
    polarity: float
    subjectivity: float
    created_at: datetime | None = None
    llm_explanation: str

    class Config:
        from_attributes = True  # ✅ Required in Pydantic v2