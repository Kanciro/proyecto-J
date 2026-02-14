from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import leccion as crud_leccion, modulo as crud_modulo, curso as crud_curso
from app.schemas.leccion import LeccionCreate, LeccionUpdate, LeccionResponse, LeccionConRecursos
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/modulo/{id_modulo}", response_model=List[LeccionConRecursos])
def get_lecciones_by_modulo(
    id_modulo: int,
    db: Session = Depends(get_db)
):
    """Obtener todas las lecciones de un módulo con sus recursos"""
    return crud_leccion.get_lecciones_by_modulo(db, id_modulo)

@router.get("/{id_leccion}", response_model=LeccionConRecursos)
def get_leccion(
    id_leccion: int,
    db: Session = Depends(get_db)
):
    """Obtener una lección por ID con sus recursos"""
    leccion = crud_leccion.get_leccion(db, id_leccion)
    if not leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )
    return leccion

@router.post("/", response_model=LeccionResponse, status_code=status.HTTP_201_CREATED)
def create_leccion(
    leccion: LeccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear una nueva lección"""
    modulo = crud_modulo.get_modulo(db, leccion.id_modulo)
    if not modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    
    curso = crud_curso.get_curso(db, modulo.id_curso)
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar lecciones a este módulo"
        )
    
    return crud_leccion.create_leccion(db, leccion)

@router.put("/{id_leccion}", response_model=LeccionResponse)
def update_leccion(
    id_leccion: int,
    leccion: LeccionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar una lección"""
    db_leccion = crud_leccion.get_leccion(db, id_leccion)
    if not db_leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )
    
    modulo = crud_modulo.get_modulo(db, db_leccion.id_modulo)
    curso = crud_curso.get_curso(db, modulo.id_curso)
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta lección"
        )
    
    return crud_leccion.update_leccion(db, id_leccion, leccion)

@router.delete("/{id_leccion}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leccion(
    id_leccion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar una lección"""
    db_leccion = crud_leccion.get_leccion(db, id_leccion)
    if not db_leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )
    
    modulo = crud_modulo.get_modulo(db, db_leccion.id_modulo)
    curso = crud_curso.get_curso(db, modulo.id_curso)
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta lección"
        )
    
    crud_leccion.delete_leccion(db, id_leccion)
    return None