from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Inscripcion(Base):
    __tablename__ = "inscripciones"
    
    id_inscripcion = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_curso = Column(Integer, ForeignKey('cursos.id_curso'), nullable=False)
    fecha_inscripcion = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    __table_args__ = (UniqueConstraint('id_estudiante', 'id_curso', name='unique_estudiante_curso'),)
    
    # Relaciones
    estudiante = relationship("Usuario", backref="inscripciones")
    curso = relationship("Curso", back_populates="inscripciones")
    progresos = relationship("ProgresoLeccion", back_populates="inscripcion", cascade="all, delete-orphan")