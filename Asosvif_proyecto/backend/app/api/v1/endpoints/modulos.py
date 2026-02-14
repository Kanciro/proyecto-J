from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import modulo as crud_modulo, curso as crud_curso
from app.schemas.modulo import ModuloCreate, ModuloUpdate, ModuloResponse, ModuloConLecciones
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/curso/{id_curso}", response_model=List[ModuloConLecciones])
def get_modulos_by_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los módulos de un curso con sus lecciones"""
    return crud_modulo.get_modulos_by_curso(db, id_curso)

@router.get("/{id_modulo}", response_model=ModuloConLecciones)
def get_modulo(
    id_modulo: int,
    db: Session = Depends(get_db)
):
    """Obtener un módulo por ID"""
    modulo = crud_modulo.get_modulo(db, id_modulo)
    if not modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    return modulo

@router.post("/", response_model=ModuloResponse, status_code=status.HTTP_201_CREATED)
def create_modulo(
    modulo: ModuloCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear un nuevo módulo"""
    curso = crud_curso.get_curso(db, modulo.id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar módulos a este curso"
        )
    
    return crud_modulo.create_modulo(db, modulo)

@router.put("/{id_modulo}", response_model=ModuloResponse)
def update_modulo(
    id_modulo: int,
    modulo: ModuloUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar un módulo"""
    db_modulo = crud_modulo.get_modulo(db, id_modulo)
    if not db_modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    
    curso = crud_curso.get_curso(db, db_modulo.id_curso)
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este módulo"
        )
    
    return crud_modulo.update_modulo(db, id_modulo, modulo)

@router.delete("/{id_modulo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_modulo(
    id_modulo: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un módulo"""
    db_modulo = crud_modulo.get_modulo(db, id_modulo)
    if not db_modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    
    curso = crud_curso.get_curso(db, db_modulo.id_curso)
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este módulo"
        )
    
    crud_modulo.delete_modulo(db, id_modulo)
    return None