from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment_pos = Column(Float, nullable=False)
    sentiment_neg = Column(Float, nullable=False)
    sentiment_neu = Column(Float, nullable=False)
    sentiment_compound = Column(Float, nullable=False)
    polarity = Column(Float, nullable=False)
    subjectivity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
