from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.leccion import LeccionResponse

class ModuloBase(BaseModel):
    titulo_modulo: str
    orden: int

class ModuloCreate(ModuloBase):
    id_curso: int

class ModuloUpdate(BaseModel):
    titulo_modulo: Optional[str] = None
    orden: Optional[int] = None

class ModuloResponse(ModuloBase):
    id_modulo: int
    id_curso: int
    
    model_config = ConfigDict(from_attributes=True)

class ModuloConLecciones(ModuloResponse):
    lecciones: List['LeccionResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)


# Actualizar referencias forward
from app.schemas.leccion import LeccionResponse
ModuloConLecciones.model_rebuild()