from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import timedelta

from ..db import models
from ..models.user import UserCreate, LoginResponse, RegisterResponse
from ..utils.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings

class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
        """Autenticar usuario con email y contraseña"""
        user = db.query(models.User).filter(models.User.email == email).first()
        
        if not user:
            return None
        
        if not user.is_active:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> models.User:
        """Crear nuevo usuario"""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = models.User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.name,  # Mapear 'name' del frontend a 'full_name' en BD
            is_active=True
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise ValueError("El email ya está registrado")
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
        """Obtener usuario por ID"""
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        """Obtener usuario por email"""
        return db.query(models.User).filter(models.User.email == email).first()
    
    @staticmethod
    def login_user(db: Session, email: str, password: str) -> LoginResponse:
        """Login completo: autenticar y generar token"""
        user = AuthService.authenticate_user(db, email, password)
        
        if not user:
            raise ValueError("Credenciales inválidas")
        
        # Crear token JWT
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="Bearer"
        )
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> RegisterResponse:
        """Registro completo de usuario"""
        try:
            # Verificar si el email ya existe
            existing_user = AuthService.get_user_by_email(db, user_data.email)
            if existing_user:
                raise ValueError("El email ya está registrado")
            
            # Crear usuario
            user = AuthService.create_user(db, user_data)
            
            return RegisterResponse(
                status="ok",
                message=f"Usuario {user.email} registrado exitosamente"
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error al registrar usuario: {str(e)}")

# Instancia global del servicio
auth_service = AuthService()