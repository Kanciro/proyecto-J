from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.usuario import RolEnum

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_completo: str
    rol: RolEnum

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[RolEnum] = None

class UsuarioInDB(UsuarioBase):
    id_usuario: int
    password_hash: str
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str