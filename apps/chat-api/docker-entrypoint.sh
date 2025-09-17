#!/bin/bash
set -e

echo "Esperando a que PostgreSQL este listo..."

# Verificar que las variables estan configuradas
if [ -z "$POSTGRES_HOST" ]; then
    echo "Error: POSTGRES_HOST no configurado"
    exit 1
fi

# Esperar a que PostgreSQL este disponible
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "PostgreSQL no esta listo - esperando..."
  sleep 2
done

echo "PostgreSQL esta listo!"

# Crear las tablas
echo "Creando tablas..."
python -c "
import sys
import os
sys.path.append('/app')
try:
    from src.db.session import engine, Base
    from src.db import models
    print('Creando tablas...')
    Base.metadata.create_all(bind=engine)
    print('Tablas creadas exitosamente')
except Exception as e:
    print(f'Error creando tablas: {e}')
    exit(1)
"

# Iniciar la aplicacion
echo "Iniciando la aplicacion en puerto 8000... (hot reload)"
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload