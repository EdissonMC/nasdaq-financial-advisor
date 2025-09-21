FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

# Instalar Python y Node.js
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y python3 python3-pip python3-venv \
    && apt-get install -y curl git

# Instalar cliente Docker
RUN apt-get update && apt-get install -y docker.io \
    && usermod -aG docker vscode

# Instalar Node.js LTS (ejemplo con 18)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Crear usuario vscode si no existe
RUN useradd -ms /bin/bash vscode || true
USER vscode

WORKDIR /workspace