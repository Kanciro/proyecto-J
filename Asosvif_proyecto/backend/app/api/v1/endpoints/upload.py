from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
from datetime import datetime
import uuid

router = APIRouter()

# Configuración
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename: str) -> bool:
    """Verificar si la extensión del archivo está permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename: str) -> str:
    """Generar un nombre de archivo único"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return unique_name

@router.post("/imagen/curso")
async def upload_curso_image(file: UploadFile = File(...)):
    """Subir imagen para portada de curso"""
    
    # Validar extensión
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión no permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validar tamaño
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo es demasiado grande. Máximo 5MB"
        )
    
    # Crear directorio si no existe
    curso_dir = os.path.join(UPLOAD_DIR, "cursos")
    os.makedirs(curso_dir, exist_ok=True)
    
    # Generar nombre único
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(curso_dir, filename)
    
    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Retornar URL
    url = f"http://localhost:8000/api/v1/upload/imagen/cursos/{filename}"
    
    return {
        "filename": filename,
        "url": url,
        "message": "Imagen subida exitosamente"
    }

@router.post("/imagen/usuario")
async def upload_usuario_image(file: UploadFile = File(...)):
    """Subir imagen de perfil de usuario"""
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión no permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo es demasiado grande. Máximo 5MB"
        )
    
    usuario_dir = os.path.join(UPLOAD_DIR, "usuarios")
    os.makedirs(usuario_dir, exist_ok=True)
    
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(usuario_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    url = f"http://localhost:8000/api/v1/upload/imagen/usuarios/{filename}"
    
    return {
        "filename": filename,
        "url": url,
        "message": "Imagen subida exitosamente"
    }

@router.post("/imagen/leccion")
async def upload_leccion_image(file: UploadFile = File(...)):
    """Subir imagen para lección"""
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión no permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo es demasiado grande. Máximo 5MB"
        )
    
    leccion_dir = os.path.join(UPLOAD_DIR, "lecciones")
    os.makedirs(leccion_dir, exist_ok=True)
    
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(leccion_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    url = f"http://localhost:8000/api/v1/upload/imagen/lecciones/{filename}"
    
    return {
        "filename": filename,
        "url": url,
        "message": "Imagen subida exitosamente"
    }

@router.get("/imagen/cursos/{filename}")
async def get_curso_image(filename: str):
    """Obtener imagen de curso"""
    file_path = os.path.join(UPLOAD_DIR, "cursos", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )
    
    return FileResponse(file_path)

@router.get("/imagen/usuarios/{filename}")
async def get_usuario_image(filename: str):
    """Obtener imagen de usuario"""
    file_path = os.path.join(UPLOAD_DIR, "usuarios", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )
    
    return FileResponse(file_path)

@router.get("/imagen/lecciones/{filename}")
async def get_leccion_image(filename: str):
    """Obtener imagen de lección"""
    file_path = os.path.join(UPLOAD_DIR, "lecciones", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )
    
    return FileResponse(file_path)

@router.delete("/imagen/{tipo}/{filename}")
async def delete_image(tipo: str, filename: str):
    """Eliminar imagen"""
    if tipo not in ["cursos", "usuarios", "lecciones"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo no válido. Use: cursos, usuarios o lecciones"
        )
    
    file_path = os.path.join(UPLOAD_DIR, tipo, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )
    
    os.remove(file_path)
    
    return {"message": "Imagen eliminada exitosamente"}