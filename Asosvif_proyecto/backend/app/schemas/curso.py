from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from app.models.curso import NivelDificultad

if TYPE_CHECKING:
    from app.schemas.modulo import ModuloResponse

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
    
    model_config = ConfigDict(from_attributes=True)

class CursoConModulos(CursoResponse):
    modulos: List['ModuloResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)

# Actualizar referencias forward
from app.schemas.modulo import ModuloResponse
CursoConModulos.model_rebuild()