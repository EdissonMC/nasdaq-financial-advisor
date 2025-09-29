FROM python:3.9-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=docker

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear script de inicialización
COPY docker-entrypoint.sh .
RUN dos2unix docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Copiar código de la aplicación
COPY . .




# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["./docker-entrypoint.sh"]