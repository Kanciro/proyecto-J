from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import progreso as crud_progreso, inscripcion as crud_inscripcion, leccion as crud_leccion
from app.schemas.progreso import ProgresoResponse, ProgresoResumen
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/inscripcion/{id_inscripcion}", response_model=List[ProgresoResponse])
def get_progreso_by_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener el progreso de una inscripción"""
    inscripcion = crud_inscripcion.get_inscripcion(db, id_inscripcion)
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada"
        )
    
    # Verificar que el usuario sea el dueño de la inscripción o admin
    if current_user.rol != "ADMIN" and inscripcion.id_estudiante != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este progreso"
        )
    
    return crud_progreso.get_progresos_by_inscripcion(db, id_inscripcion)

@router.post("/completar/{id_leccion}", response_model=ProgresoResponse)
def marcar_leccion_completada(
    id_leccion: int,
    id_inscripcion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Marcar una lección como completada"""
    # Verificar que la lección existe
    leccion = crud_leccion.get_leccion(db, id_leccion)
    if not leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )
    
    # Verificar que la inscripción existe
    inscripcion = crud_inscripcion.get_inscripcion(db, id_inscripcion)
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada"
        )
    
    # Verificar que el usuario sea el dueño de la inscripción
    if inscripcion.id_estudiante != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este progreso"
        )
    
    return crud_progreso.marcar_leccion_completada(db, id_inscripcion, id_leccion)

@router.post("/actualizar-vista/{id_leccion}", response_model=ProgresoResponse)
def actualizar_ultima_vista(
    id_leccion: int,
    id_inscripcion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar la última vez que se vio una lección"""
    # Verificar que la inscripción existe y pertenece al usuario
    inscripcion = crud_inscripcion.get_inscripcion(db, id_inscripcion)
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada"
        )
    
    if inscripcion.id_estudiante != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este progreso"
        )
    
    return crud_progreso.actualizar_ultima_vista(db, id_inscripcion, id_leccion)

@router.get("/resumen/{id_curso}", response_model=ProgresoResumen)
def get_resumen_progreso(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener resumen del progreso en un curso"""
    # Verificar inscripción
    inscripcion = crud_inscripcion.get_inscripcion_by_estudiante_curso(
        db, current_user.id_usuario, id_curso
    )
    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No estás inscrito en este curso"
        )
    
    # Obtener progresos
    progresos = crud_progreso.get_progresos_by_inscripcion(db, inscripcion.id_inscripcion)
    
    # Calcular total de lecciones del curso
    from app.models.modulo import Modulo
    from app.models.leccion import Leccion
    total_lecciones = db.query(Leccion).join(Modulo).filter(Modulo.id_curso == id_curso).count()
    
    lecciones_completadas = sum(1 for p in progresos if p.completada)
    porcentaje = (lecciones_completadas / total_lecciones * 100) if total_lecciones > 0 else 0
    
    return ProgresoResumen(
        total_lecciones=total_lecciones,
        lecciones_completadas=lecciones_completadas,
        porcentaje_completado=round(porcentaje, 2)
    )