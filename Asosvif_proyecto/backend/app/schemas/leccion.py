from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.recurso import RecursoResponse

class LeccionBase(BaseModel):
    titulo_leccion: str
    orden: int
    descripcion_breve: Optional[str] = None

class LeccionCreate(LeccionBase):
    id_modulo: int

class LeccionUpdate(BaseModel):
    titulo_leccion: Optional[str] = None
    orden: Optional[int] = None
    descripcion_breve: Optional[str] = None

class LeccionResponse(LeccionBase):
    id_leccion: int
    id_modulo: int
    
    model_config = ConfigDict(from_attributes=True)

class LeccionConRecursos(LeccionResponse):
    recursos: List['RecursoResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)


# Actualizar referencias forward
from app.schemas.recurso import RecursoResponse
LeccionConRecursos.model_rebuild()