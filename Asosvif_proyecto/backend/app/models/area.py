from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class AreaHidroponia(Base):
    __tablename__ = "areas_hidroponia"
    
    id_area = Column(Integer, primary_key=True, autoincrement=True)
    nombre_area = Column(String(100), unique=True, nullable=False)
    
    # Relaciones
    cursos = relationship("Curso", back_populates="area")