from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InscripcionBase(BaseModel):
    id_curso: int

class InscripcionCreate(InscripcionBase):
    pass

class InscripcionResponse(InscripcionBase):
    id_inscripcion: int
    id_estudiante: int
    fecha_inscripcion: datetime
    
    class Config:
        from_attributes = True