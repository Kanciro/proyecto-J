from sqlalchemy.orm import Session
from app.models.modulo import Modulo
from app.schemas.modulo import ModuloCreate, ModuloUpdate
from typing import Optional, List

def get_modulo(db: Session, id_modulo: int) -> Optional[Modulo]:
    return db.query(Modulo).filter(Modulo.id_modulo == id_modulo).first()

def get_modulos_by_curso(db: Session, id_curso: int) -> List[Modulo]:
    return db.query(Modulo).filter(Modulo.id_curso == id_curso).order_by(Modulo.orden).all()

def create_modulo(db: Session, modulo: ModuloCreate) -> Modulo:
    db_modulo = Modulo(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

def update_modulo(db: Session, id_modulo: int, modulo: ModuloUpdate) -> Optional[Modulo]:
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        return None
    
    update_data = modulo.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_modulo, field, value)
    
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

def delete_modulo(db: Session, id_modulo: int) -> bool:
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        return False
    
    db.delete(db_modulo)
    db.commit()
    return True