from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from .database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    question = Column(Text, nullable=False)
    retrieved_chunks = Column(JSON, nullable=True)  # list of chunk ids / metadata
    final_answer = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    token_usage = Column(Integer, nullable=True)
    sentiment_label = Column(String(32), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    keywords = Column(JSON, nullable=True)  # list of extracted keywords
    topic = Column(String(128), nullable=True)
    rating = Column(Integer, nullable=True)
