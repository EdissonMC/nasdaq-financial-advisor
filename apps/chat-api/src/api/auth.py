from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db, Base, engine
from ..db import models
from ..models.user import UserCreate, UserLogin, LoginResponse, RegisterResponse, UserRead, ErrorResponse
from ..services.auth_service import AuthService
from .dependencies import get_current_active_user

# Crear el router para autenticación
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Crear las tablas en la base de datos (solo para desarrollo)
# En producción esto se hace con Alembic
Base.metadata.create_all(bind=engine)

@router.post("/register", 
             response_model=RegisterResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Registrar nuevo usuario",
             description="Crear una nueva cuenta de usuario en el sistema")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario en el sistema.
    
    - **name**: Nombre completo del usuario
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    """
    try:
        response = AuthService.register_user(db, user_data)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login",
             response_model=LoginResponse,
             summary="Iniciar sesión",
             description="Autenticar usuario y obtener token de acceso")
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con email y contraseña.
    
    - **email**: Email del usuario registrado
    - **password**: Contraseña del usuario
    
    Retorna un token JWT válido por 24 horas.
    """
    try:
        response = AuthService.login_user(db, user_data.email, user_data.password)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/me",
            response_model=UserRead,
            summary="Obtener perfil del usuario",
            description="Obtener información del usuario autenticado")
async def get_current_user_profile(
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Obtener el perfil del usuario actualmente autenticado.
    
    Requiere token JWT válido en el header Authorization.
    """
    return current_user

@router.get("/verify",
            summary="Verificar token",
            description="Verificar si el token JWT es válido")
async def verify_token(
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Verificar si el token JWT proporcionado es válido.
    
    Retorna información básica del usuario si el token es válido.
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "message": "Token válido"
    }

@router.post("/logout",
             summary="Cerrar sesión",
             description="Cerrar sesión del usuario (invalidar token)")
async def logout(
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Cerrar sesión del usuario.
    
    Nota: Como JWT es stateless, el token seguirá siendo válido hasta que expire.
    En el frontend se debe eliminar el token del almacenamiento local.
    """
    return {
        "message": "Sesión cerrada exitosamente",
        "user_id": current_user.id
    }

# Endpoint para healthcheck del servicio de auth
@router.get("/health",
            summary="Estado del servicio de autenticación",
            description="Verificar si el servicio de autenticación está funcionando")
async def auth_health_check():
    """
    Verificar el estado del servicio de autenticación.
    """
    return {
        "status": "healthy",
        "service": "auth",
        "message": "Servicio de autenticación funcionando correctamente"
    }