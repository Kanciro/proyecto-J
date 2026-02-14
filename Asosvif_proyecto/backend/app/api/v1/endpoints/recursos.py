from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import recurso as crud_recurso, leccion as crud_leccion, modulo as crud_modulo, curso as crud_curso
from app.schemas.recurso import RecursoCreate, RecursoUpdate, RecursoResponse
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/leccion/{id_leccion}", response_model=List[RecursoResponse])
def get_recursos_by_leccion(
    id_leccion: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los recursos de una lección"""
    return crud_recurso.get_recursos_by_leccion(db, id_leccion)

@router.get("/{id_recurso}", response_model=RecursoResponse)
def get_recurso(
    id_recurso: int,
    db: Session = Depends(get_db)
):
    """Obtener un recurso por ID"""
    recurso = crud_recurso.get_recurso(db, id_recurso)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    return recurso

@router.post("/", response_model=RecursoResponse, status_code=status.HTTP_201_CREATED)
def create_recurso(
    recurso: RecursoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear un nuevo recurso"""
    leccion = crud_leccion.get_leccion(db, recurso.id_leccion)
    if not leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )
    
    modulo = crud_modulo.get_modulo(db, leccion.id_modulo)
    curso = crud_curso.get_curso(db, modulo.id_curso)
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar recursos a esta lección"
        )
    
    return crud_recurso.create_recurso(db, recurso)

@router.put("/{id_recurso}", response_model=RecursoResponse)
def update_recurso(
    id_recurso: int,
    recurso: RecursoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar un recurso"""
    db_recurso = crud_recurso.get_recurso(db, id_recurso)
    if not db_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    leccion = crud_leccion.get_leccion(db, db_recurso.id_leccion)
    modulo = crud_modulo.get_modulo(db, leccion.id_modulo)
    curso = crud_curso.get_curso(db, modulo.id_curso)
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este recurso"
        )
    
    return crud_recurso.update_recurso(db, id_recurso, recurso)

@router.delete("/{id_recurso}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurso(
    id_recurso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un recurso"""
    db_recurso = crud_recurso.get_recurso(db, id_recurso)
    if not db_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    leccion = crud_leccion.get_leccion(db, db_recurso.id_leccion)
    modulo = crud_modulo.get_modulo(db, leccion.id_modulo)
    curso = crud_curso.get_curso(db, modulo.id_curso)
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este recurso"
        )
    
    crud_recurso.delete_recurso(db, id_recurso)
    return None