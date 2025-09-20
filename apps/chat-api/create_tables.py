import sys
import os
import traceback
import psycopg2
from src.core.config import settings

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.db.session import engine, Base
from src.db import models

def create_tables():
    print("🔄 Creando tablas en la base de datos...")
    print(f"🧪 Python FS encoding: {sys.getfilesystemencoding()}, stdout: {getattr(sys.stdout, 'encoding', None)}")
    print(f"🔧 DB URL: {settings.database_url}")
    
    try:
        # Prueba de conexión directa con psycopg2 para aislar errores de encoding
        try:
            # Evitar que PGOPTIONS del entorno afecte a esta prueba
            os.environ.pop("PGOPTIONS", None)
            
            conn = psycopg2.connect(settings.database_url)

            with conn.cursor() as cur:
                cur.execute("SHOW server_version; SHOW server_encoding; SHOW client_encoding;")
                rows = [r for r in cur]
                print(f"✅ psycopg2 connect OK. Info: {rows}")
            conn.close()
        except Exception as e:
            print("❌ Falla conexión psycopg2 directa:")
            print(repr(e))
            traceback.print_exc()

        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        
        # Mostrar tablas creadas
        tables = list(Base.metadata.tables.keys())
        print(f"📋 Tablas creadas: {tables}")
        
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_tables()