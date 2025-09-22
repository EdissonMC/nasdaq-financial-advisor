from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

logger = logging.getLogger(__name__)

# ✅ CHANGE: PostgreSQL instead of SQLite
def get_database_url():
    """Build PostgreSQL URL from environment variables"""
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_user = os.getenv("POSTGRES_USER", "chatapi_user")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "chatapi_password")
    postgres_db = os.getenv("POSTGRES_DB", "chatapi_db")
    
    return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}?client_encoding=utf8"

DATABASE_URL = get_database_url()

# Engine configured for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=os.getenv("DEBUG", "false").lower() == "true",
    # UTF-8 encoding configuration
    connect_args={
        "client_encoding": "utf8",
        "options": "-c timezone=UTC"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Sentiment analysis tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise
