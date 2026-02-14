from sqlalchemy import Column, Integer, String, Text, Enum, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class NivelDificultad(str, enum.Enum):
    BASICO = "BÁSICO"
    INTERMEDIO = "INTERMEDIO"
    AVANZADO = "AVANZADO"

class Curso(Base):
    __tablename__ = "cursos"
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    id_instructor = Column(Integer, ForeignKey('instructores.id_instructor'), nullable=False)
    id_area = Column(Integer, ForeignKey('areas_hidroponia.id_area'), nullable=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    nivel_dificultad = Column(Enum(NivelDificultad), nullable=False)
    url_portada = Column(Text, nullable=True)
    puntuacion_media = Column(DECIMAL(2, 1), default=0.0)
    fecha_publicacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    instructor = relationship("Instructor", back_populates="cursos")
    area = relationship("AreaHidroponia", back_populates="cursos")
    modulos = relationship("Modulo", back_populates="curso", cascade="all, delete-orphan")
    inscripciones = relationship("Inscripcion", back_populates="curso")
    calificaciones = relationship("Calificacion", back_populates="curso")