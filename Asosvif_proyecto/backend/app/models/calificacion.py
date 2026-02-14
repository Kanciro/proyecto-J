from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Calificacion(Base):
    __tablename__ = "calificaciones"
    
    id_calificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_curso = Column(Integer, ForeignKey('cursos.id_curso'), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    fecha_calificacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='check_puntuacion'),
        UniqueConstraint('id_estudiante', 'id_curso', name='unique_estudiante_curso_calificacion'),
    )
    
    # Relaciones
    estudiante = relationship("Usuario", backref="calificaciones")
    curso = relationship("Curso", back_populates="calificaciones")