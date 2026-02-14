from pydantic import BaseModel
from typing import Optional, List

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
    
    class Config:
        from_attributes = True

class LeccionConRecursos(LeccionResponse):
    recursos: List['RecursoResponse'] = []
    
    class Config:
        from_attributes = True