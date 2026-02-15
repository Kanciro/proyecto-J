from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.calificacion import Calificacion
from app.crud import curso as crud_curso, inscripcion as crud_inscripcion
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

class CalificacionCreate(BaseModel):
    id_curso: int
    puntuacion: int

class CalificacionResponse(BaseModel):
    id_calificacion: int
    id_estudiante: int
    id_curso: int
    puntuacion: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=CalificacionResponse, status_code=status.HTTP_201_CREATED)
def crear_calificacion(
    calificacion: CalificacionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear o actualizar calificación de un curso"""
    # Verificar que el curso existe
    curso = crud_curso.get_curso(db, calificacion.id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar que el usuario está inscrito
    inscripcion = crud_inscripcion.get_inscripcion_by_estudiante_curso(
        db, current_user.id_usuario, calificacion.id_curso
    )
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes estar inscrito en el curso para calificarlo"
        )
    
    # Validar puntuación
    if calificacion.puntuacion < 1 or calificacion.puntuacion > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La puntuación debe estar entre 1 y 5"
        )
    
    # Buscar si ya existe una calificación
    calificacion_existente = db.query(Calificacion).filter(
        Calificacion.id_estudiante == current_user.id_usuario,
        Calificacion.id_curso == calificacion.id_curso
    ).first()
    
    if calificacion_existente:
        # Actualizar calificación existente
        calificacion_existente.puntuacion = calificacion.puntuacion
        db.commit()
        db.refresh(calificacion_existente)
        db_calificacion = calificacion_existente
    else:
        # Crear nueva calificación
        db_calificacion = Calificacion(
            id_estudiante=current_user.id_usuario,
            id_curso=calificacion.id_curso,
            puntuacion=calificacion.puntuacion
        )
        db.add(db_calificacion)
        db.commit()
        db.refresh(db_calificacion)
    
    # Actualizar puntuación media del curso
    crud_curso.actualizar_puntuacion_curso(db, calificacion.id_curso)
    
    return db_calificacion

@router.get("/curso/{id_curso}", response_model=List[CalificacionResponse])
def get_calificaciones_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """Obtener todas las calificaciones de un curso"""
    return db.query(Calificacion).filter(Calificacion.id_curso == id_curso).all()

@router.get("/mi-calificacion/{id_curso}")
def get_mi_calificacion(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener la calificación del usuario actual para un curso"""
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_estudiante == current_user.id_usuario,
        Calificacion.id_curso == id_curso
    ).first()
    
    if not calificacion:
        return {"calificado": False, "puntuacion": None}
    
    return {"calificado": True, "puntuacion": calificacion.puntuacion}