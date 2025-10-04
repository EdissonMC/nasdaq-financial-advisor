
# --- Development stage ---
FROM python:3.9-slim AS dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=development
WORKDIR /app
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear script de inicialización
COPY docker-entrypoint.sh .
RUN dos2unix docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Copiar código de la aplicación
COPY . .

EXPOSE 8000
CMD ["./docker-entrypoint.sh"]

# --- Production stage ---
FROM python:3.9-slim AS prod
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
WORKDIR /app
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000
CMD ["./docker-entrypoint.sh"]