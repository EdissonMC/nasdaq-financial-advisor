# 🚀 Guía de Despliegue en EC2

## Opción 1: Despliegue Automático (Recomendado)

### Paso 1: Localiza tu llave SSH
Busca el archivo `financial-chatbot-key.pem` en:
- Carpeta de Descargas
- `~/.ssh/`
- Donde lo guardaste cuando creaste la instancia EC2

### Paso 2: Actualiza el script
Edita el archivo `connect-and-deploy.sh` y cambia esta línea:
```bash
PEM_KEY="/ruta/a/tu/financial-chatbot-key.pem"  # 👈 Pon la ruta correcta aquí
```

### Paso 3: Ejecuta el script
```bash
cd nasdaq-financial-advisor
bash connect-and-deploy.sh
```

¡Listo! El script se encargará de todo.

---

## Opción 2: Despliegue Manual

### Paso 1: Conectarse a EC2
```bash
ssh -i /ruta/a/tu/financial-chatbot-key.pem ubuntu@23.22.180.200
```

### Paso 2: Actualizar el código
```bash
cd ~/nasdaq-financial-advisor
git fetch origin
git pull origin develop
```

### Paso 3: Actualizar configuración de AWS
```bash
cd ~/nasdaq-financial-advisor/apps/chat-api

# Hacer backup del .env actual
cp .env .env.backup

# Editar el archivo .env
nano .env
```

Cambia estas líneas:
```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

Guarda con `Ctrl+X`, luego `Y`, luego `Enter`

### Paso 4: Reiniciar servicios
```bash
cd ~/nasdaq-financial-advisor

# Detener contenedores
docker compose down

# Reconstruir y levantar
docker compose up -d --build

# Esperar unos segundos...
sleep 10

# Verificar estado
docker compose ps
```

### Paso 5: Verificar que funciona
```bash
# Ver logs
docker compose logs chat-api --tail 50

# Probar health check
curl http://localhost:8000/health

# Probar chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":{"role":"user","content":"Hello, what is a stock?"}}'
```

---

## 🔍 Encontrar tu llave SSH

### En Windows (Git Bash):
```bash
# Buscar en Descargas
ls ~/Downloads/*.pem

# Buscar en toda tu carpeta de usuario
find ~ -name "*.pem" 2>/dev/null

# Buscar en ubicaciones comunes
ls /c/Users/*/Downloads/*.pem
ls /c/Users/*/.ssh/*.pem
```

### En Linux/Mac:
```bash
# Buscar en home
find ~ -name "financial-chatbot-key.pem"

# Buscar en Descargas
ls ~/Downloads/*.pem
```

---

## ⚠️ Solución de problemas comunes

### Error: "Permission denied (publickey)"
Tu llave no tiene los permisos correctos:
```bash
chmod 400 /ruta/a/tu/financial-chatbot-key.pem
```

### Error: "No such file or directory"
La ruta a tu llave `.pem` es incorrecta. Búscala con los comandos de arriba.

### Los contenedores no inician
```bash
# Ver qué salió mal
docker compose logs

# Verificar que Docker esté corriendo
docker ps

# Reiniciar Docker
sudo systemctl restart docker
```

### El chat no responde
```bash
# Ver logs del backend
docker compose logs chat-api --tail 100

# Verificar variables de entorno
docker compose exec chat-api env | grep AWS
docker compose exec chat-api env | grep BEDROCK
```

---

## 📊 Comandos útiles después del despliegue

```bash
# Ver todos los logs en tiempo real
docker compose logs -f

# Ver solo logs del backend
docker compose logs -f chat-api

# Ver estado de todos los servicios
docker compose ps

# Reiniciar un servicio específico
docker compose restart chat-api

# Entrar a un contenedor
docker compose exec chat-api bash

# Ver uso de recursos
docker stats

# Limpiar logs y recursos
docker system prune -a
```

---

## 🎯 Checklist de Verificación

Después del despliegue, verifica:

- [ ] Todos los contenedores están corriendo (`docker compose ps`)
- [ ] Backend responde en puerto 8000 (`curl http://localhost:8000/health`)
- [ ] Frontend responde en puerto 5173 (acceder desde navegador)
- [ ] Chat funciona correctamente (probar endpoint)
- [ ] Logs no muestran errores críticos
- [ ] AWS region es `us-east-1`
- [ ] Bedrock model es `anthropic.claude-3-haiku-20240307-v1:0`

---

## 🌐 Acceder desde Internet

Una vez verificado que todo funciona localmente en EC2, necesitas:

1. **Configurar Security Groups** en AWS Console:
   - Puerto 22 (SSH) - Solo tu IP
   - Puerto 80 (HTTP) - 0.0.0.0/0
   - Puerto 443 (HTTPS) - 0.0.0.0/0
   - Puerto 8000 (Backend API) - 0.0.0.0/0
   - Puerto 5173 (Frontend) - 0.0.0.0/0

2. **Acceder**:
   - Backend: `http://23.22.180.200:8000`
   - Frontend: `http://23.22.180.200:5173`
   - API Docs: `http://23.22.180.200:8000/docs`

---

¿Necesitas ayuda? Revisa los logs con `docker compose logs -f`
