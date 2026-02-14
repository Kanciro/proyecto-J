from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Instructor(Base):
    __tablename__ = "instructores"
    
    id_instructor = Column(Integer, ForeignKey('usuarios.id_usuario'), primary_key=True)
    biografia = Column(Text, nullable=True)
    url_foto_perfil = Column(Text, nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", backref="instructor")
    cursos = relationship("Curso", back_populates="instructor")