# Frontend - Asesor Financiero (Vite + React + TS)

## Requisitos
- Node.js 18+

## Variables de entorno
Crea `.env` a partir de `.env.example`:
```
VITE_CHAT_API_URL=http://localhost:8000
```

Opcionales en UI (⚙️ Config):
- URL del Chat API
- Timeout (ms)
- Top K
- Simulación local si no hay conexión
- Auth Token (si el backend requiere Authorization)

## Login (opcional)
- Usa el botón "Iniciar sesión" para autenticarte contra `POST /auth/login`.
- Tras el login, el token se guarda en configuración y se envía como `Authorization` en todas las llamadas.
- Para cerrar sesión, pulsa "Cerrar sesión" (el token se borra de la configuración).

## Instalación y scripts
```
cd frontend
npm install
npm run dev
```
Aplicación en `http://localhost:5173`.

Build y preview:
```
npm run build
npm run preview
```

## Docker
```
# build (desde la raíz o carpeta frontend)
docker build -t finchat-frontend ./frontend
# run
docker run --rm -p 8080:80 finchat-frontend
```

## Docker Compose (con Chat API mock)
```
docker compose up --build
# Frontend: http://localhost:5173
# Chat API mock: http://localhost:8000/docs
```

## Estructura clave
- `src/modules/app/App.tsx`: shell de la app
- `src/modules/chat/*`: componentes de chat
- `src/services/api.ts`: cliente API (/chat y /chat/history) con fallback local
- `src/styles/global.css`: estilos base
