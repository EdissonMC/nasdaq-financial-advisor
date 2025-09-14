from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar configuración
from .core.config import settings

# Importar routers
try:
    from .api import routes
    routes_available = True
except ImportError:
    routes_available = False

from .api import auth

app = FastAPI(
    title=settings.app_name,
    description="API del Financial AI Chatbot con autenticación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir routers
if routes_available:
    app.include_router(routes.router)

# Incluir el router de autenticación
app.include_router(auth.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Financial AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "auth": "/auth"
    }

# Health check general
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Financial AI Chatbot API",
        "version": "1.0.0",
        "database": "PostgreSQL",
        "authentication": "JWT"
    }