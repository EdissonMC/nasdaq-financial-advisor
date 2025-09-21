from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings
import os

# Asegurar codificación UTF-8 en el cliente para evitar errores de Unicode en Windows/psycopg2
os.environ.setdefault("PGCLIENTENCODING", "UTF8")
os.environ.setdefault("PGOPTIONS", "-c client_encoding=UTF8 -c lc_messages=C")

# Engine configurado para PostgreSQL
engine = create_engine(
    settings.database_url,
    pool_size=10,                    # Conexiones en el pool
    max_overflow=20,                 # Conexiones adicionales
    pool_recycle=3600,              # Reciclar conexiones cada hora
    pool_pre_ping=True,             # Verificar conexiones antes de usar
    echo=settings.debug,            # Mostrar queries SQL en debug
    # Forzar codificación UTF-8 en la sesión de PostgreSQL
    connect_args={
        "options": "-c client_encoding=UTF8 -c lc_messages=C"
    },
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class para los modelos ORM
Base = declarative_base()

# Dependency para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()