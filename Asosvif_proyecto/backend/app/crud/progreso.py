from sqlalchemy.orm import Session
from app.models.progreso import ProgresoLeccion
from typing import Optional, List

def get_progreso(db: Session, id_progreso: int) -> Optional[ProgresoLeccion]:
    return db.query(ProgresoLeccion).filter(ProgresoLeccion.id_progreso == id_progreso).first()

def get_progreso_by_inscripcion_leccion(db: Session, id_inscripcion: int, id_leccion: int) -> Optional[ProgresoLeccion]:
    return db.query(ProgresoLeccion).filter(
        ProgresoLeccion.id_inscripcion == id_inscripcion,
        ProgresoLeccion.id_leccion == id_leccion
    ).first()

def get_progresos_by_inscripcion(db: Session, id_inscripcion: int) -> List[ProgresoLeccion]:
    return db.query(ProgresoLeccion).filter(ProgresoLeccion.id_inscripcion == id_inscripcion).all()

def marcar_leccion_completada(db: Session, id_inscripcion: int, id_leccion: int) -> ProgresoLeccion:
    progreso = get_progreso_by_inscripcion_leccion(db, id_inscripcion, id_leccion)
    
    if not progreso:
        progreso = ProgresoLeccion(
            id_inscripcion=id_inscripcion,
            id_leccion=id_leccion,
            completada=True
        )
        db.add(progreso)
    else:
        progreso.completada = True # type: ignore
    
    db.commit()
    db.refresh(progreso)
    return progreso

def actualizar_ultima_vista(db: Session, id_inscripcion: int, id_leccion: int) -> ProgresoLeccion:
    progreso = get_progreso_by_inscripcion_leccion(db, id_inscripcion, id_leccion)
    
    if not progreso:
        progreso = ProgresoLeccion(
            id_inscripcion=id_inscripcion,
            id_leccion=id_leccion,
            completada=False
        )
        db.add(progreso)
    
    db.commit()
    db.refresh(progreso)
    return progreso