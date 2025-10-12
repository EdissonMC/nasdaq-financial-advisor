#!/bin/bash
# Script para actualizar la instancia EC2 con los últimos cambios

set -e  # Salir si hay algún error

echo "🚀 Actualizando instancia EC2..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navegar al proyecto
echo -e "${BLUE}📂 Navegando al directorio del proyecto...${NC}"
cd ~/nasdaq-financial-advisor

# Hacer pull de los cambios
echo -e "${BLUE}⬇️  Descargando últimos cambios...${NC}"
git fetch origin
git pull origin develop

# Verificar estado
echo -e "${BLUE}📋 Estado del repositorio:${NC}"
git status

# Actualizar archivo .env del backend
echo -e "${YELLOW}⚙️  Actualizando configuración de AWS...${NC}"
cd ~/nasdaq-financial-advisor/apps/chat-api

# Crear backup del .env actual
if [ -f .env ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup del .env creado"
fi

# Actualizar las variables críticas en el .env
echo -e "${BLUE}📝 Actualizando AWS_REGION y BEDROCK_MODEL_ID...${NC}"
sed -i 's/AWS_REGION=us-west-1/AWS_REGION=us-east-1/g' .env
sed -i 's/BEDROCK_MODEL_ID=.*/BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0/g' .env

echo "✅ Configuración actualizada:"
grep "AWS_REGION" .env
grep "BEDROCK_MODEL_ID" .env

# Volver a la raíz del proyecto
cd ~/nasdaq-financial-advisor

# Detener contenedores actuales
echo -e "${BLUE}🛑 Deteniendo contenedores actuales...${NC}"
docker compose down

# Reconstruir y levantar todos los servicios
echo -e "${BLUE}🔨 Reconstruyendo y levantando servicios...${NC}"
docker compose up -d --build

# Esperar a que los servicios inicien
echo -e "${YELLOW}⏳ Esperando a que los servicios inicien...${NC}"
sleep 10

# Verificar estado de los contenedores
echo -e "${BLUE}📊 Estado de los contenedores:${NC}"
docker compose ps

# Verificar logs del backend
echo -e "${BLUE}📜 Últimos logs del backend:${NC}"
docker compose logs chat-api --tail 30

# Probar el endpoint de salud
echo -e "${BLUE}🏥 Probando endpoint de salud...${NC}"
sleep 5
curl -s http://localhost:8000/health | jq '.' || echo "⚠️  El endpoint de salud no responde aún"

# Probar el chat
echo -e "${BLUE}💬 Probando endpoint de chat...${NC}"
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":{"role":"user","content":"Hello, what is a stock?"}}')

if echo "$CHAT_RESPONSE" | grep -q "assistant"; then
    echo -e "${GREEN}✅ Chat funcionando correctamente!${NC}"
    echo "Respuesta: $(echo $CHAT_RESPONSE | jq -r '.message.content' | head -c 100)..."
else
    echo -e "${YELLOW}⚠️  Error en el chat:${NC}"
    echo "$CHAT_RESPONSE"
fi

echo ""
echo -e "${GREEN}✅ Despliegue completado!${NC}"
echo ""
echo "📝 Comandos útiles:"
echo "  - Ver logs: docker compose logs -f chat-api"
echo "  - Ver estado: docker compose ps"
echo "  - Reiniciar: docker compose restart"
echo "  - Ver todos los logs: docker compose logs -f"
