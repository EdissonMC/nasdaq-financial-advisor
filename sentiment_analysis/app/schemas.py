from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class AnalysisOut(BaseModel):
    id: int
    text: str
    sentiment: Dict[str, float]
    bow: Dict[str, int]
    blob_polarity: Dict[str, float]
    polarity: float
    subjectivity: float
    created_at: datetime

    class Config:
        orm_mode = True

