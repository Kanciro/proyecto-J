from sqlalchemy.orm import Session
from app.models.leccion import Leccion
from app.schemas.leccion import LeccionCreate, LeccionUpdate
from typing import Optional, List

def get_leccion(db: Session, id_leccion: int) -> Optional[Leccion]:
    return db.query(Leccion).filter(Leccion.id_leccion == id_leccion).first()

def get_lecciones_by_modulo(db: Session, id_modulo: int) -> List[Leccion]:
    return db.query(Leccion).filter(Leccion.id_modulo == id_modulo).order_by(Leccion.orden).all()

def create_leccion(db: Session, leccion: LeccionCreate) -> Leccion:
    db_leccion = Leccion(**leccion.dict())
    db.add(db_leccion)
    db.commit()
    db.refresh(db_leccion)
    return db_leccion

def update_leccion(db: Session, id_leccion: int, leccion: LeccionUpdate) -> Optional[Leccion]:
    db_leccion = get_leccion(db, id_leccion)
    if not db_leccion:
        return None
    
    update_data = leccion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_leccion, field, value)
    
    db.commit()
    db.refresh(db_leccion)
    return db_leccion

def delete_leccion(db: Session, id_leccion: int) -> bool:
    db_leccion = get_leccion(db, id_leccion)
    if not db_leccion:
        return False
    
    db.delete(db_leccion)
    db.commit()
    return True