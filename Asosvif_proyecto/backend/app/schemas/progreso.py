from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProgresoBase(BaseModel):
    id_leccion: int
    completada: bool = False

class ProgresoCreate(BaseModel):
    id_leccion: int

class ProgresoUpdate(BaseModel):
    completada: Optional[bool] = None

class ProgresoResponse(BaseModel):
    id_progreso: int
    id_inscripcion: int
    id_leccion: int
    completada: bool
    ultima_vista_en: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProgresoResumen(BaseModel):
    """Resumen del progreso de un curso"""
    total_lecciones: int
    lecciones_completadas: int
    porcentaje_completado: float