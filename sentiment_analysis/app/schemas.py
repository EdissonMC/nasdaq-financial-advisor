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
    user_id: int | None = None

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
    user_id: int | None = None

    class Config:
        from_attributes = True  # ✅ Required in Pydantic v2

from typing import List, Optional


class DashboardMetrics(BaseModel):
    avg_positive: float
    avg_negative: float
    avg_neutral: float
    avg_compound: float

class DashboardChartData(BaseModel):
    sentiment_compound: List[float]
    polarity: List[float]
    subjectivity: List[float]
    created_at: List[datetime]

class AdminDashboardData(BaseModel):
    records: List[SentimentAnalysis]
    metrics: DashboardMetrics
    charts: DashboardChartData