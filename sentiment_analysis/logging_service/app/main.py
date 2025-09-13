from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, analysis
from typing import List
import os

# create DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Logging & Analysis Service")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/log_interaction", response_model=schemas.InteractionOut)
def log_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    # analyze sentiment
    label, score = analysis.analyze_sentiment(payload.question)
    # create keywords for the single question (lightweight: top words in that question)
    kw = []
    try:
        # Use simple split; for per-question keywords we return top tokens
        kw = [w for w in payload.question.lower().split() if len(w) > 2][:10]
    except Exception:
        kw = []

    db_obj = models.Interaction(
        user_id=payload.user_id,
        question=payload.question,
        retrieved_chunks=payload.retrieved_chunks,
        final_answer=payload.final_answer,
        latency_ms=payload.latency_ms,
        token_usage=payload.token_usage,
        sentiment_label=label,
        sentiment_score=score,
        keywords=kw,
        rating=payload.rating,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/interactions/", response_model=List[schemas.InteractionOut])
def list_interactions(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(models.Interaction).order_by(models.Interaction.timestamp.desc()).limit(limit).all()
    return rows

@app.get("/analytics/top_keywords")
def top_keywords(n: int = 20, db: Session = Depends(get_db)):
    rows = db.query(models.Interaction).all()
    questions = [r.question for r in rows]
    term_count = analysis.extract_keywords_bow(questions, top_n=n)
    return {"top_keywords": [{"term": t, "count": int(c)} for t, c in term_count]}

@app.get("/analytics/sentiment_trend")
def sentiment_trend(db: Session = Depends(get_db)):
    rows = db.query(models.Interaction).all()
    total = len(rows)
    pos = sum(1 for r in rows if r.sentiment_label == "positive")
    neg = sum(1 for r in rows if r.sentiment_label == "negative")
    neu = sum(1 for r in rows if r.sentiment_label == "neutral")
    return {"total": total, "positive": pos, "negative": neg, "neutral": neu}

@app.get("/analytics/company_counts")
def company_counts(db: Session = Depends(get_db)):
    """
    Simple heuristic: count mentions by company ticker-like tokens found in questions.
    Better approach: use NER or canonical list of tickers. This is a simple quick metric.
    """
    rows = db.query(models.Interaction).all()
    freq = {}
    for r in rows:
        q = (r.question or "").upper()
        # crude heuristic: any all-caps 2-5 letters token maybe ticker
        tokens = [t for t in q.split() if t.isalpha() and 1 < len(t) <= 5 and t.isupper()]
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
    # sort
    items = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    return {"company_like_counts": [{"token": k, "count": v} for k, v in items[:20]]}
