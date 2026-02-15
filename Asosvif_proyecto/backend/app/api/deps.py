from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.crud.usuario import get_usuario_by_email
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    """
    Obtener el usuario actual desde el token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = get_usuario_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """
    Obtener el usuario actual activo
    Por ahora todos los usuarios están activos
    """
    # Aquí podrías agregar verificación de usuario activo
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

def get_current_admin_user(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    """
    Verificar que el usuario actual es administrador
    """
    if current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user

def get_current_instructor_user(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    """
    Verificar que el usuario actual es instructor
    """
    if current_user.rol not in ["INSTRUCTOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes ser instructor o administrador"
        )
    return current_user

def get_current_estudiante_user(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    """
    Verificar que el usuario actual es estudiante
    """
    if current_user.rol not in ["ESTUDIANTE", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes ser estudiante"
        )
    return current_user