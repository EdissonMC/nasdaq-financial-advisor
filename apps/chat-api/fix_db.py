#!/usr/bin/env python3
"""
Solución definitiva para el problema de encoding con PostgreSQL
"""
import os
import psycopg2
from urllib.parse import quote_plus
import locale

def configure_environment():
    """Configurar variables de entorno para evitar problemas de encoding"""
    # Forzar inglés para evitar caracteres especiales en mensajes de error
    os.environ['LC_ALL'] = 'C'
    os.environ['LC_MESSAGES'] = 'C'  # Específico para mensajes
    os.environ['LANG'] = 'C'
    os.environ['LANGUAGE'] = 'en'    # Forzar inglés
    
    # PostgreSQL específico
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    os.environ['PGLOCALEDIR'] = ''   # Usar mensajes por defecto
    
    print("🔧 Environment configured:")
    for key in ['LC_ALL', 'LC_MESSAGES', 'LANG', 'LANGUAGE', 'PGCLIENTENCODING']:
        print(f"   {key}: {os.environ.get(key, 'Not set')}")

def test_connection_with_safe_error_handling():
    """Test conexión con manejo seguro de errores"""
    print("\n🔧 Testing connection with safe error handling...")
    
    configure_environment()
    
    try:
        # Intentar conexión con configuración específica
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='chatapi_db',
            user='chatapi_user',
            password='chatapi_password',
            # Configuraciones específicas para evitar problemas de encoding
            options='-c client_encoding=utf8 -c lc_messages=C'
        )
        
        print('✅ Connection successful with safe error handling!')
        
        cursor = conn.cursor()
        cursor.execute("SHOW lc_messages;")
        lc_messages = cursor.fetchone()[0]
        print(f"📊 PostgreSQL lc_messages: {lc_messages}")
        
        cursor.execute("SHOW client_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"📊 PostgreSQL client_encoding: {encoding}")
        
        cursor.close()
        conn.close()
        return True
        
    except UnicodeDecodeError as e:
        print(f'❌ Unicode error persists: {e}')
        print("🔧 Trying alternative approach...")
        return test_with_binary_mode()
        
    except Exception as e:
        # Convertir error a string de forma segura
        try:
            error_msg = str(e)
        except UnicodeDecodeError:
            error_msg = repr(e)
        print(f'❌ Connection failed: {error_msg}')
        return False

def test_with_binary_mode():
    """Test usando modo binario para evitar problemas de encoding"""
    print("\n🔧 Testing with binary mode...")
    
    try:
        # Usar psycopg2 con configuración más específica
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='chatapi_db',
            user='chatapi_user',
            password='chatapi_password',
            client_encoding='utf8'
        )
        
        # Configurar la sesión para usar mensajes en inglés
        cursor = conn.cursor()
        cursor.execute("SET lc_messages TO 'C';")
        cursor.execute("SET client_encoding TO 'UTF8';")
        
        print('✅ Connection successful with binary mode!')
        
        # Test query
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"📊 PostgreSQL version: {result[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Binary mode failed: {repr(e)}')
        return False

def test_docker_container_fix():
    """Test sugiriendo fixes en el contenedor Docker"""
    print("\n🔧 Docker container fixes needed...")
    
    docker_commands = [
        "# Fix 1: Restart container with English locale",
        "docker exec -it chatapi-postgres bash -c \"echo 'export LC_ALL=C' >> /etc/environment\"",
        "",
        "# Fix 2: Set PostgreSQL configuration",
        "docker exec -it chatapi-postgres bash -c \"echo \\\"lc_messages = 'C'\\\" >> /var/lib/postgresql/data/postgresql.conf\"",
        "",
        "# Fix 3: Restart PostgreSQL service",
        "docker exec -it chatapi-postgres bash -c \"pg_ctl reload -D /var/lib/postgresql/data\"",
        "",
        "# Fix 4: Alternative - restart entire container",
        "docker restart chatapi-postgres",
    ]
    
    for cmd in docker_commands:
        print(cmd)
    
    return False

def create_fixed_connection_function():
    """Crear función de conexión que funcione"""
    print("\n🔧 Creating fixed connection function...")
    
    connection_code = '''
def get_database_connection():
    """
    Función de conexión que maneja problemas de encoding
    """
    import os
    import psycopg2
    from urllib.parse import quote_plus
    
    # Configurar environment
    os.environ['LC_ALL'] = 'C'
    os.environ['LC_MESSAGES'] = 'C'
    os.environ['LANG'] = 'C'
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='chatapi_db',
            user='chatapi_user',
            password='chatapi_password',
            options='-c client_encoding=utf8 -c lc_messages=C'
        )
        
        # Configurar sesión
        cursor = conn.cursor()
        cursor.execute("SET lc_messages TO 'C';")
        cursor.execute("SET client_encoding TO 'UTF8';")
        cursor.close()
        
        return conn
        
    except Exception as e:
        print(f"Database connection error: {repr(e)}")
        raise
'''
    
    print("Copy this function to your code:")
    print(connection_code)

def main():
    print("🚀 PostgreSQL Encoding Problem - Advanced Diagnosis\n")
    
    # Test 1: Configuración mejorada
    result1 = test_connection_with_safe_error_handling()
    
    if not result1:
        # Test 2: Docker container fixes
        print("\n" + "="*50)
        print("DOCKER CONTAINER NEEDS CONFIGURATION CHANGES")
        print("="*50)
        test_docker_container_fix()
        
        # Crear función de conexión fixed
        create_fixed_connection_function()
        
        print("\n" + "="*50)
        print("IMMEDIATE SOLUTION")
        print("="*50)
        print("1. Ejecuta estos comandos para fix temporal:")
        print("   docker exec -it chatapi-postgres bash -c \"export LC_ALL=C && pg_ctl reload\"")
        print("   docker restart chatapi-postgres")
        print("\n2. O usa la función de conexión personalizada mostrada arriba")

if __name__ == "__main__":
    main()