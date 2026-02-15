from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import inscripcion as crud_inscripcion, curso as crud_curso
from app.schemas.inscripcion import InscripcionCreate, InscripcionResponse
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/mis-cursos", response_model=List[InscripcionResponse])
def get_mis_inscripciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener todas las inscripciones del usuario actual"""
    return crud_inscripcion.get_inscripciones_by_estudiante(db, current_user.id_usuario)

@router.get("/curso/{id_curso}", response_model=List[InscripcionResponse])
def get_inscripciones_by_curso(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener todas las inscripciones de un curso (solo instructor o admin)"""
    curso = crud_curso.get_curso(db, id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    if current_user.rol != "ADMIN" and curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver las inscripciones de este curso"
        )
    
    return crud_inscripcion.get_inscripciones_by_curso(db, id_curso)

@router.post("/", response_model=InscripcionResponse, status_code=status.HTTP_201_CREATED)
def create_inscripcion(
    inscripcion: InscripcionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Inscribirse a un curso"""
    # Verificar que el curso existe
    curso = crud_curso.get_curso(db, inscripcion.id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar si ya está inscrito
    inscripcion_existente = crud_inscripcion.get_inscripcion_by_estudiante_curso(
        db, current_user.id_usuario, inscripcion.id_curso
    )
    if inscripcion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya estás inscrito en este curso"
        )
    
    return crud_inscripcion.create_inscripcion(db, inscripcion, current_user.id_usuario)

@router.delete("/{id_inscripcion}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Cancelar inscripción a un curso"""
    inscripcion = crud_inscripcion.get_inscripcion(db, id_inscripcion)
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada"
        )
    
    # Solo el estudiante inscrito o un admin pueden cancelar
    if current_user.rol != "ADMIN" and inscripcion.id_estudiante != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cancelar esta inscripción"
        )
    
    crud_inscripcion.delete_inscripcion(db, id_inscripcion)
    return None

@router.get("/verificar/{id_curso}", response_model=bool)
def verificar_inscripcion(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Verificar si el usuario está inscrito en un curso"""
    inscripcion = crud_inscripcion.get_inscripcion_by_estudiante_curso(
        db, current_user.id_usuario, id_curso
    )
    return inscripcion is not None