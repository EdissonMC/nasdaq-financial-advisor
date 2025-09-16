from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file (stored locally)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sentiment.db"

# SQLite requires the "check_same_thread" flag
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
