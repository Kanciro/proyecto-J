from pydantic import BaseModel
from typing import Optional, List

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
    
    class Config:
        from_attributes = True

class ModuloConLecciones(ModuloResponse):
    lecciones: List['LeccionResponse'] = []
    
    class Config:
        from_attributes = True