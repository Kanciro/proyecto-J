from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProgresoLeccion(Base):
    __tablename__ = "progreso_lecciones"
    
    id_progreso = Column(BigInteger, primary_key=True, autoincrement=True)
    id_inscripcion = Column(Integer, ForeignKey('inscripciones.id_inscripcion'), nullable=False)
    id_leccion = Column(Integer, ForeignKey('lecciones.id_leccion'), nullable=False)
    completada = Column(Boolean, default=False)
    ultima_vista_en = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (UniqueConstraint('id_inscripcion', 'id_leccion', name='unique_inscripcion_leccion'),)
    
    # Relaciones
    inscripcion = relationship("Inscripcion", back_populates="progresos")
    leccion = relationship("Leccion", back_populates="progresos")