from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    usuarios,
    cursos,
    modulos,
    lecciones,
    recursos,
    inscripciones,
    progreso,
    calificaciones,
    mensajes,
    upload  # NUEVO
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(upload.router, prefix="/upload", tags=["Subir Archivos"])  # NUEVO
api_router.include_router(cursos.router, prefix="/cursos", tags=["Cursos"])
api_router.include_router(modulos.router, prefix="/modulos", tags=["Módulos"])
api_router.include_router(lecciones.router, prefix="/lecciones", tags=["Lecciones"])
api_router.include_router(recursos.router, prefix="/recursos", tags=["Recursos"])
api_router.include_router(inscripciones.router, prefix="/inscripciones", tags=["Inscripciones"])
api_router.include_router(progreso.router, prefix="/progreso", tags=["Progreso"])
api_router.include_router(calificaciones.router, prefix="/calificaciones", tags=["Calificaciones"])
api_router.include_router(mensajes.router, prefix="/mensajes", tags=["Mensajes y Comentarios"])