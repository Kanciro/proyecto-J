from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class TipoRecurso(str, enum.Enum):
    VIDEO = "VIDEO"
    TEXTO_ENRIQUECIDO = "TEXTO_ENRIQUECIDO"
    PDF = "PDF"
    ENLACE_EXTERNO = "ENLACE_EXTERNO"
    CODIGO_ZIP = "CODIGO_ZIP"

class RecursoLeccion(Base):
    __tablename__ = "recursos_leccion"
    
    id_recurso = Column(Integer, primary_key=True, autoincrement=True)
    id_leccion = Column(Integer, ForeignKey('lecciones.id_leccion'), nullable=False)
    tipo_recurso = Column(Enum(TipoRecurso), nullable=False)
    titulo_recurso = Column(String(255), nullable=True)
    contenido_texto = Column(Text, nullable=True)
    url_recurso = Column(Text, nullable=True)
    orden = Column(Integer, nullable=False, default=1)
    
    # Relaciones
    leccion = relationship("Leccion", back_populates="recursos")