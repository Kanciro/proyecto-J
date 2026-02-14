from sqlalchemy import Column, Integer, Text, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ComentarioMensaje(Base):
    __tablename__ = "comentarios_y_mensajes"
    
    id_mensaje = Column(Integer, primary_key=True, autoincrement=True)
    id_remitente = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_destinatario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=True)
    id_leccion = Column(Integer, ForeignKey('lecciones.id_leccion'), nullable=True)
    contenido = Column(Text, nullable=False)
    es_privado = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    remitente = relationship("Usuario", foreign_keys=[id_remitente], backref="mensajes_enviados")
    destinatario = relationship("Usuario", foreign_keys=[id_destinatario], backref="mensajes_recibidos")
    leccion = relationship("Leccion", back_populates="mensajes")

# Crear índice
Index('idx_comentarios_leccion', ComentarioMensaje.id_leccion)