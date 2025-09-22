FROM python:3.10-slim

WORKDIR /app
# NEW: Python environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ ADD: Download NLTK data
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"
RUN python -c "import nltk; nltk.download('punkt', quiet=True)"

# Copy app code
COPY ./app ./app
COPY ./dashboard ./dashboard
RUN mkdir -p /app/data
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]