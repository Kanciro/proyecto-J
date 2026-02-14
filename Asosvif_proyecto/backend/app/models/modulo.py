from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Modulo(Base):
    __tablename__ = "modulos"
    
    id_modulo = Column(Integer, primary_key=True, autoincrement=True)
    id_curso = Column(Integer, ForeignKey('cursos.id_curso'), nullable=False)
    titulo_modulo = Column(String(255), nullable=False)
    orden = Column(Integer, nullable=False)
    
    __table_args__ = (UniqueConstraint('id_curso', 'orden', name='unique_curso_orden'),)
    
    # Relaciones
    curso = relationship("Curso", back_populates="modulos")
    lecciones = relationship("Leccion", back_populates="modulo", cascade="all, delete-orphan")