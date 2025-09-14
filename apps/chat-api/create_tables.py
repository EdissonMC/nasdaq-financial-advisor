import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.db.session import engine, Base
from src.db import models

def create_tables():
    print("🔄 Creando tablas en la base de datos...")
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        
        # Mostrar tablas creadas
        tables = list(Base.metadata.tables.keys())
        print(f"📋 Tablas creadas: {tables}")
        
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False

if __name__ == "__main__":
    create_tables()