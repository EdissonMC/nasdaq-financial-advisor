#!/usr/bin/env python3
"""
Test de conexión a PostgreSQL
"""
import os
import psycopg2
from urllib.parse import quote_plus

# Configurar encoding antes de cualquier conexión
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['LC_ALL'] = 'C'
os.environ['LANG'] = 'C'

def test_direct_connection():
    """Test conexión directa"""
    print("🔧 Testing direct connection...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='chatapi_db',
            user='chatapi_user',
            password='chatapi_password',
            client_encoding='utf8'
        )
        print('✅ Direct connection successful')
        
        # Test simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"📊 PostgreSQL version: {result[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Direct connection failed: {e}')
        print(f'❌ Error type: {type(e).__name__}')
        return False

def test_url_connection():
    """Test conexión con URL"""
    print("\n🔧 Testing URL connection...")
    
    # Construir URL similar a tu settings
    password = quote_plus('chatapi_password')
    database_url = f"postgresql://chatapi_user:{password}@localhost:5432/chatapi_db?client_encoding=utf8"
    
    print(f"🔗 Database URL: {database_url}")
    
    try:
        conn = psycopg2.connect(database_url)
        print('✅ URL connection successful')
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), current_user;")
        result = cursor.fetchone()
        print(f"📊 Database: {result[0]}, User: {result[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ URL connection failed: {e}')
        print(f'❌ Error type: {type(e).__name__}')
        return False

def test_encoding():
    """Test encoding específico"""
    print("\n🔧 Testing encoding handling...")
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='chatapi_db',
            user='chatapi_user',
            password='chatapi_password',
            client_encoding='utf8'
        )
        
        cursor = conn.cursor()
        
        # Test caracteres especiales
        cursor.execute("SELECT 'Hola José, ¿cómo estás?' as test_text;")
        result = cursor.fetchone()
        print(f"✅ Encoding test: {result[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Encoding test failed: {e}')
        return False

def main():
    print("🚀 Starting PostgreSQL connection tests...\n")
    
    # Mostrar configuración del entorno
    print("🔍 Environment check:")
    print(f"   PGCLIENTENCODING: {os.environ.get('PGCLIENTENCODING', 'Not set')}")
    print(f"   LC_ALL: {os.environ.get('LC_ALL', 'Not set')}")
    print(f"   LANG: {os.environ.get('LANG', 'Not set')}")
    print()
    
    # Ejecutar tests
    test1 = test_direct_connection()
    test2 = test_url_connection()
    test3 = test_encoding()
    
    print("\n📋 Summary:")
    print(f"   Direct connection: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   URL connection: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"   Encoding test: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! Your connection should work.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()