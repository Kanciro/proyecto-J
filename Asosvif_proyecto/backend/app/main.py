from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear directorio de uploads si no existe
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/cursos", exist_ok=True)
os.makedirs("uploads/usuarios", exist_ok=True)
os.makedirs("uploads/lecciones", exist_ok=True)

# Crear las tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas de base de datos verificadas/creadas exitosamente")
except Exception as e:
    logger.error(f"Error al crear tablas: {e}")

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para plataforma de cursos de hidroponía",
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:4200",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar directorio de archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Incluir los routers de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a la API de Hidroponía",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "api": "running",
        "database": "connected"
    }

@app.get("/info", tags=["Info"])
def api_info():
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "API REST para plataforma de cursos de hidroponía",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "health": "/health"
        },
        "api_v1": settings.API_V1_STR,
        "features": [
            "Autenticación JWT",
            "Gestión de usuarios",
            "CRUD de cursos",
            "Sistema de inscripciones",
            "Subida de imágenes"
        ]
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Recurso no encontrado",
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Error interno del servidor: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor"
        }
    )

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Iniciando {settings.APP_NAME}")
    logger.info(f"📚 Documentación: http://localhost:8000/docs")
    logger.info(f"🗄️  Base de datos: {settings.DB_NAME}")
    logger.info(f"📁 Directorio uploads: /uploads")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"👋 Cerrando {settings.APP_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )