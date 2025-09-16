from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Example: "postgresql://user:password@db:5432/logging_db"
POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/logging_db"
)

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (for FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
