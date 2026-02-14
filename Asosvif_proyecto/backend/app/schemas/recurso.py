from pydantic import BaseModel
from typing import Optional
from app.models.recurso import TipoRecurso

class RecursoBase(BaseModel):
    tipo_recurso: TipoRecurso
    titulo_recurso: Optional[str] = None
    contenido_texto: Optional[str] = None
    url_recurso: Optional[str] = None
    orden: int = 1

class RecursoCreate(RecursoBase):
    id_leccion: int

class RecursoUpdate(BaseModel):
    tipo_recurso: Optional[TipoRecurso] = None
    titulo_recurso: Optional[str] = None
    contenido_texto: Optional[str] = None
    url_recurso: Optional[str] = None
    orden: Optional[int] = None

class RecursoResponse(RecursoBase):
    id_recurso: int
    id_leccion: int
    
    class Config:
        from_attributes = True