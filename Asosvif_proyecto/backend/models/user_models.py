# models/user_models.py
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid # Para manejar los UUIDs

# Definición de la enumeración para el rol
import enum
class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    INSTRUCTOR = "INSTRUCTOR"
    ESTUDIANTE = "ESTUDIANTE"

class Usuario(Base):
    __tablename__ = "usuarios"

    # Supabase usa UUIDs, así que usamos el tipo UUID de PostgreSQL
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False)
    rol = Column(Enum(UserRole), nullable=False)
    
    # Relación uno a uno con la tabla instructores (si aplica)
    instructor = relationship("Instructor", back_populates="usuario", uselist=False)
    
    # Relaciones con otras tablas (inscripciones, calificaciones, etc.)
    inscripciones = relationship("Inscripcion", back_populates="estudiante")
    calificaciones = relationship("Calificacion", back_populates="estudiante")
    remitidos = relationship("ComentarioYMensaje", foreign_keys='ComentarioYMensaje.id_remitente', back_populates="remitente")
    destinatarios = relationship("ComentarioYMensaje", foreign_keys='ComentarioYMensaje.id_destinatario', back_populates="destinatario")

class Instructor(Base):
    __tablename__ = "instructores"

    id_instructor = Column(UUID(as_uuid=True), ForeignKey('usuarios.id_usuario'), primary_key=True)
    biografia = Column(String)
    url_foto_perfil = Column(String)
    
    # Relación inversa a la tabla usuarios
    usuario = relationship("Usuario", back_populates="instructor")
    
    # Relación uno a muchos con cursos
    cursos = relationship("Curso", back_populates="instructor")