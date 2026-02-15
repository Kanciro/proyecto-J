from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.usuario import usuario as crud_usuario
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario, RolEnum

router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return current_user

@router.put("/me", response_model=UsuarioResponse)
def update_current_user(
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar información del usuario actual"""
    # No permitir cambiar el rol a través de este endpoint
    if usuario_update.rol is not None and current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cambiar tu rol"
        )
    
    updated_user = crud_usuario.update(
        db=db,
        db_obj=current_user,
        obj_in=usuario_update
    )
    
    return updated_user

@router.get("/", response_model=List[UsuarioResponse])
def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener lista de usuarios (solo admin)"""
    if current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta información"
        )
    
    usuarios = crud_usuario.get_multi(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def get_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener un usuario por ID"""
    usuario = crud_usuario.get_by_id(db, id_usuario=id_usuario)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Solo admin o el mismo usuario pueden ver la info completa
    if current_user.rol != "ADMIN" and current_user.id_usuario != id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta información"
        )
    
    return usuario

@router.put("/{id_usuario}", response_model=UsuarioResponse)
def update_usuario(
    id_usuario: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar un usuario (solo admin)"""
    if current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden actualizar usuarios"
        )
    
    usuario = crud_usuario.get_by_id(db, id_usuario=id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    updated_user = crud_usuario.update(
        db=db,
        db_obj=usuario,
        obj_in=usuario_update
    )
    
    return updated_user

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un usuario (solo admin)"""
    if current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar usuarios"
        )
    
    usuario = crud_usuario.get_by_id(db, id_usuario=id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir eliminar el propio usuario admin
    if usuario.id_usuario == current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta de administrador"
        )
    
    crud_usuario.delete(db, id=id_usuario)
    return None

@router.get("/rol/{rol}", response_model=List[UsuarioResponse])
def get_usuarios_by_rol(
    rol: RolEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener usuarios por rol (solo admin)"""
    if current_user.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta información"
        )
    
    usuarios = crud_usuario.get_multi_by_rol(db, rol=rol, skip=skip, limit=limit)
    return usuarios

@router.get("/instructores/lista", response_model=List[UsuarioResponse])
def get_instructores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista pública de instructores"""
    usuarios = crud_usuario.get_multi_by_rol(
        db, 
        rol=RolEnum.INSTRUCTOR, 
        skip=skip, 
        limit=limit
    )
    return usuarios