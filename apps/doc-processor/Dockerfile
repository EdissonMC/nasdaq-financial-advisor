FROM python:3.11-slim
WORKDIR /workspace
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt
# Torch CPU para sentence-transformers
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
COPY app ./app
