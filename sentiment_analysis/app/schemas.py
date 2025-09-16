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

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
