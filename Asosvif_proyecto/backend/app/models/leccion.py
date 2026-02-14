from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Leccion(Base):
    __tablename__ = "lecciones"
    
    id_leccion = Column(Integer, primary_key=True, autoincrement=True)
    id_modulo = Column(Integer, ForeignKey('modulos.id_modulo'), nullable=False)
    titulo_leccion = Column(String(255), nullable=False)
    orden = Column(Integer, nullable=False)
    descripcion_breve = Column(Text, nullable=True)
    
    __table_args__ = (UniqueConstraint('id_modulo', 'orden', name='unique_modulo_orden'),)
    
    # Relaciones
    modulo = relationship("Modulo", back_populates="lecciones")
    recursos = relationship("RecursoLeccion", back_populates="leccion", cascade="all, delete-orphan")
    progresos = relationship("ProgresoLeccion", back_populates="leccion")
    mensajes = relationship("ComentarioMensaje", back_populates="leccion")