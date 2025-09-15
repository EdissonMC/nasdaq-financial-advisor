"""
Script para configurar la base de datos PostgreSQL
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.core.config import settings

def create_database():
    """Crear la base de datos si no existe"""
    try:
        # Conectar a PostgreSQL sin especificar base de datos
        conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database='postgres'  # Base de datos por defecto
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.postgres_db}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {settings.postgres_db}")
            print(f"✅ Base de datos '{settings.postgres_db}' creada exitosamente")
        else:
            print(f"ℹ️  Base de datos '{settings.postgres_db}' ya existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_database()