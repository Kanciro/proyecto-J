from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos (solo para desarrollo)
# En producción se recomienda usar Alembic para migraciones
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

# Configurar CORS (Cross-Origin Resource Sharing)
# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React (Create React App)
        "http://localhost:5173",      # Vite
        "http://localhost:4200",      # Angular
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir los routers de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    """Endpoint de bienvenida"""
    return {
        "message": "Bienvenido a la API de Hidroponía",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Verificar el estado de la API"""
    return {
        "status": "ok",
        "api": "running",
        "database": "connected"
    }

# Endpoint de información de la API
@app.get("/info", tags=["Info"])
def api_info():
    """Información general de la API"""
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "API REST para plataforma de cursos de hidroponía estilo Platzi",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "health": "/health"
        },
        "api_v1": settings.API_V1_STR,
        "features": [
            "Autenticación JWT",
            "Gestión de usuarios (Admin, Instructor, Estudiante)",
            "CRUD completo de cursos, módulos, lecciones",
            "Sistema de inscripciones",
            "Seguimiento de progreso",
            "Sistema de calificaciones",
            "Mensajería y comentarios"
        ]
    }

# Manejador global de errores 404
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

# Manejador global de errores 500
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Error interno del servidor: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "message": "Por favor contacta al administrador"
        }
    )

# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """Ejecutar al iniciar la aplicación"""
    logger.info(f"🚀 Iniciando {settings.APP_NAME}")
    logger.info(f"📚 Documentación disponible en: http://localhost:8000/docs")
    logger.info(f"🔧 Modo DEBUG: {settings.DEBUG}")
    logger.info(f"🗄️  Base de datos: {settings.DB_NAME}")

# Evento de cierre de la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    """Ejecutar al cerrar la aplicación"""
    logger.info(f"👋 Cerrando {settings.APP_NAME}")

# Si ejecutas este archivo directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )