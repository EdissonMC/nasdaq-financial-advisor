#!/bin/bash
# Script para conectarse a la instancia EC2 y ejecutar el despliegue

# INSTRUCCIONES:
# 1. Reemplaza /ruta/a/tu/llave.pem con la ubicación real de tu archivo .pem
# 2. Ejecuta: bash connect-and-deploy.sh

set -e

# Configuración
EC2_IP="23.22.180.200"
EC2_USER="ubuntu"
PEM_KEY="/c/_EDISON/PROYECTOS/FINANCIAL_AI_CHATBOT/financial-chatbot-key.pem"  # 👈 CAMBIAR ESTO

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔗 Conectando a la instancia EC2...${NC}"
echo "IP: $EC2_IP"
echo ""

# Verificar que la llave existe
if [ ! -f "$PEM_KEY" ]; then
    echo -e "${RED}❌ Error: No se encuentra el archivo $PEM_KEY${NC}"
    echo ""
    echo "Busca tu archivo .pem y actualiza la variable PEM_KEY en este script"
    echo ""
    echo "Ubicaciones comunes:"
    echo "  - ~/Downloads/financial-chatbot-key.pem"
    echo "  - ~/.ssh/financial-chatbot-key.pem"
    echo "  - C:/Users/TU_USUARIO/Downloads/financial-chatbot-key.pem"
    exit 1
fi

# Verificar permisos de la llave
chmod 400 "$PEM_KEY"

# Copiar el script de despliegue a EC2
echo -e "${BLUE}📤 Copiando script de despliegue a EC2...${NC}"
scp -i "$PEM_KEY" deploy-to-ec2.sh ${EC2_USER}@${EC2_IP}:~/

# Conectar y ejecutar el script
echo -e "${BLUE}🚀 Ejecutando despliegue en EC2...${NC}"
ssh -i "$PEM_KEY" ${EC2_USER}@${EC2_IP} "bash ~/deploy-to-ec2.sh"

echo ""
echo -e "${GREEN}✅ Despliegue completado!${NC}"
echo ""
echo "Para conectarte manualmente a EC2:"
echo "  ssh -i $PEM_KEY ${EC2_USER}@${EC2_IP}"
