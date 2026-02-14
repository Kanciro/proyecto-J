from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from models.user_models import UserRole

# 1. Esquema Base (Campos comunes)
class UserBase(BaseModel):
    email: EmailStr
    nombre_completo: str
    rol: UserRole = UserRole.ESTUDIANTE

# 2. Esquema para el REGISTRO (Pide todo)
class UserCreate(UserBase):
    password: str

# 3. NUEVO: Esquema para el LOGIN (Solo lo necesario)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 4. Esquema para RESPUESTA (Lo que el backend devuelve al frontend)
class UserOut(BaseModel):
    id_usuario: UUID
    email: EmailStr
    nombre_completo: str
    rol: UserRole

    class Config:
        from_attributes = True # Permite que Pydantic lea modelos de SQLAlchemy