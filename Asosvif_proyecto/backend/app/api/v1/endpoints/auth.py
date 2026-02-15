from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.crud.usuario import usuario as crud_usuario, authenticate_usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.schemas.token import Token
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el usuario ya existe
    db_usuario = crud_usuario.get_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear nuevo usuario
    return crud_usuario.create(db=db, obj_in=usuario)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con email y contraseña
    OAuth2 compatible con username (que será el email)
    """
    # Autenticar usuario
    user = authenticate_usuario(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id_usuario}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/login-json", response_model=Token)
def login_json(
    usuario_login: UsuarioLogin,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con JSON (alternativa a form-data)
    """
    # Autenticar usuario
    user = authenticate_usuario(db, email=usuario_login.email, password=usuario_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id_usuario}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Refrescar el token de acceso
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email, "id": current_user.id_usuario}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/verify")
def verify_token(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Verificar si el token es válido
    """
    return {
        "valid": True,
        "user": {
            "id_usuario": current_user.id_usuario,
            "email": current_user.email,
            "nombre_completo": current_user.nombre_completo,
            "rol": current_user.rol
        }
    }

@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_active_user)):
    """
    Cerrar sesión (en el cliente se debe eliminar el token)
    """
    return {
        "message": "Sesión cerrada exitosamente. Elimina el token del almacenamiento local."
    }