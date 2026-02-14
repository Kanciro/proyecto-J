from sqlalchemy.orm import Session
from app.models.inscripcion import Inscripcion
from app.schemas.inscripcion import InscripcionCreate
from typing import Optional, List

def get_inscripcion(db: Session, id_inscripcion: int) -> Optional[Inscripcion]:
    return db.query(Inscripcion).filter(Inscripcion.id_inscripcion == id_inscripcion).first()

def get_inscripciones_by_estudiante(db: Session, id_estudiante: int) -> List[Inscripcion]:
    return db.query(Inscripcion).filter(Inscripcion.id_estudiante == id_estudiante).all()

def get_inscripciones_by_curso(db: Session, id_curso: int) -> List[Inscripcion]:
    return db.query(Inscripcion).filter(Inscripcion.id_curso == id_curso).all()

def get_inscripcion_by_estudiante_curso(db: Session, id_estudiante: int, id_curso: int) -> Optional[Inscripcion]:
    return db.query(Inscripcion).filter(
        Inscripcion.id_estudiante == id_estudiante,
        Inscripcion.id_curso == id_curso
    ).first()

def create_inscripcion(db: Session, inscripcion: InscripcionCreate, id_estudiante: int) -> Inscripcion:
    db_inscripcion = Inscripcion(
        id_estudiante=id_estudiante,
        id_curso=inscripcion.id_curso
    )
    db.add(db_inscripcion)
    db.commit()
    db.refresh(db_inscripcion)
    return db_inscripcion

def delete_inscripcion(db: Session, id_inscripcion: int) -> bool:
    db_inscripcion = get_inscripcion(db, id_inscripcion)
    if not db_inscripcion:
        return False
    
    db.delete(db_inscripcion)
    db.commit()
    return True