from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.curso import NivelDificultad

class CursoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    nivel_dificultad: NivelDificultad
    id_area: Optional[int] = None
    url_portada: Optional[str] = None

class CursoCreate(CursoBase):
    id_instructor: int

class CursoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    nivel_dificultad: Optional[NivelDificultad] = None
    id_area: Optional[int] = None
    url_portada: Optional[str] = None

class CursoResponse(CursoBase):
    id_curso: int
    id_instructor: int
    puntuacion_media: float
    fecha_publicacion: datetime
    
    class Config:
        from_attributes = True

class CursoConModulos(CursoResponse):
    modulos: List['ModuloResponse'] = []
    
    class Config:
        from_attributes = True