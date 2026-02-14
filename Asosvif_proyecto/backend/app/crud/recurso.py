from sqlalchemy.orm import Session
from app.models.recurso import RecursoLeccion
from app.schemas.recurso import RecursoCreate, RecursoUpdate
from typing import Optional, List

def get_recurso(db: Session, id_recurso: int) -> Optional[RecursoLeccion]:
    return db.query(RecursoLeccion).filter(RecursoLeccion.id_recurso == id_recurso).first()

def get_recursos_by_leccion(db: Session, id_leccion: int) -> List[RecursoLeccion]:
    return db.query(RecursoLeccion).filter(RecursoLeccion.id_leccion == id_leccion).order_by(RecursoLeccion.orden).all()

def create_recurso(db: Session, recurso: RecursoCreate) -> RecursoLeccion:
    db_recurso = RecursoLeccion(**recurso.dict())
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

def update_recurso(db: Session, id_recurso: int, recurso: RecursoUpdate) -> Optional[RecursoLeccion]:
    db_recurso = get_recurso(db, id_recurso)
    if not db_recurso:
        return None
    
    update_data = recurso.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recurso, field, value)
    
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

def delete_recurso(db: Session, id_recurso: int) -> bool:
    db_recurso = get_recurso(db, id_recurso)
    if not db_recurso:
        return False
    
    db.delete(db_recurso)
    db.commit()
    return True