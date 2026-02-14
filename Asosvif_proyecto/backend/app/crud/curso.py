from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.curso import Curso
from app.models.calificacion import Calificacion
from app.schemas.curso import CursoCreate, CursoUpdate
from typing import Optional, List

def get_curso(db: Session, id_curso: int) -> Optional[Curso]:
    return db.query(Curso).filter(Curso.id_curso == id_curso).first()

def get_cursos(db: Session, skip: int = 0, limit: int = 100) -> List[Curso]:
    return db.query(Curso).offset(skip).limit(limit).all()

def get_cursos_by_instructor(db: Session, id_instructor: int) -> List[Curso]:
    return db.query(Curso).filter(Curso.id_instructor == id_instructor).all()

def get_cursos_by_area(db: Session, id_area: int) -> List[Curso]:
    return db.query(Curso).filter(Curso.id_area == id_area).all()

def create_curso(db: Session, curso: CursoCreate) -> Curso:
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def update_curso(db: Session, id_curso: int, curso: CursoUpdate) -> Optional[Curso]:
    db_curso = get_curso(db, id_curso)
    if not db_curso:
        return None
    
    update_data = curso.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_curso, field, value)
    
    db.commit()
    db.refresh(db_curso)
    return db_curso

def delete_curso(db: Session, id_curso: int) -> bool:
    db_curso = get_curso(db, id_curso)
    if not db_curso:
        return False
    
    db.delete(db_curso)
    db.commit()
    return True

def actualizar_puntuacion_curso(db: Session, id_curso: int):
    """Calcula y actualiza la puntuación media del curso"""
    puntuacion_media = db.query(func.avg(Calificacion.puntuacion))\
        .filter(Calificacion.id_curso == id_curso)\
        .scalar()
    
    if puntuacion_media:
        db_curso = get_curso(db, id_curso)
        db_curso.puntuacion_media = round(puntuacion_media, 1)
        db.commit()