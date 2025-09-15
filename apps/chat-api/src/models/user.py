from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# AJUSTADO: Para registro - el frontend envía "name" no "full_name"
class UserCreate(BaseModel):
    name: str  # Cambiado de full_name a name
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        return v.lower().strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name is required')
        return v.strip()

# Para mostrar información del usuario
class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    
    class Config:
        orm_mode = True

# AJUSTADO: Login response - exactamente lo que espera el frontend
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

# AJUSTADO: Register response - lo que espera el frontend
class RegisterResponse(BaseModel):
    status: str = "ok"
    message: Optional[str] = None

# Para login (request)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    @validator('email', pre=True)
    def normalize_email(cls, v):
        return v.lower().strip() if v else v

# Datos del token JWT
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

# Para manejo de errores consistente
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None