

# --- Development stage (para desarrollo local, NO TOCAR) ---
FROM python:3.10-slim AS dev
WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"
RUN python -c "import nltk; nltk.download('punkt', quiet=True)"
COPY ./app ./app
COPY ./dashboard ./dashboard
RUN mkdir -p /app/data
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

# --- Builder stage (solo para producción) ---
FROM python:3.10-slim AS builder
WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# Instala compiladores y dependencias de build SOLO aquí
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"
RUN python -c "import nltk; nltk.download('punkt', quiet=True)"
COPY ./app ./app
COPY ./dashboard ./dashboard
RUN mkdir -p /app/data

# --- Production stage ---
FROM python:3.10-slim AS prod
WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# Solo instala dependencias mínimas del sistema (sin compiladores)
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
# Copia solo los paquetes instalados desde builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Copia solo el código fuente necesario
COPY ./app ./app
COPY ./dashboard ./dashboard
RUN mkdir -p /app/data
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]