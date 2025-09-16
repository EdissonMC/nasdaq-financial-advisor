from sqlalchemy import Column, Integer, String, JSON, Float, DateTime, func
from .database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    # Sentiment data
    sentiment = Column(JSON, nullable=False)
    bow = Column(JSON, nullable=False)
    blob_polarity = Column(JSON, nullable=False)

    # Extra fields for easier querying
    polarity = Column(Float, nullable=False)
    subjectivity = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

