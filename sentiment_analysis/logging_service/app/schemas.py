from pydantic import BaseModel
from typing import Optional, List, Any

class InteractionCreate(BaseModel):
    user_id: Optional[str]
    question: str
    retrieved_chunks: Optional[List[Any]] = None
    final_answer: Optional[str] = None
    latency_ms: Optional[int] = None
    token_usage: Optional[int] = None
    rating: Optional[int] = None

class InteractionOut(BaseModel):
    id: int
    user_id: Optional[str]
    timestamp: str
    question: str
    final_answer: Optional[str]
    sentiment_label: Optional[str]
    sentiment_score: Optional[float]
    keywords: Optional[List[str]]

    class Config:
        orm_mode = True
