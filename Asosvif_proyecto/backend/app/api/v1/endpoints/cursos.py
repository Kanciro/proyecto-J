from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import curso as crud_curso
from app.schemas.curso import CursoCreate, CursoUpdate, CursoResponse, CursoConModulos
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/", response_model=List[CursoResponse])
def get_cursos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los cursos"""
    cursos = crud_curso.get_cursos(db, skip=skip, limit=limit)
    return cursos

@router.get("/{id_curso}", response_model=CursoConModulos)
def get_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """Obtener un curso por ID con sus módulos"""
    curso = crud_curso.get_curso(db, id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    return curso

@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create_curso(
    curso: CursoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear un nuevo curso (solo instructores)"""
    if current_user.rol not in ["INSTRUCTOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo instructores pueden crear cursos"
        )
    
    return crud_curso.create_curso(db, curso)

@router.put("/{id_curso}", response_model=CursoResponse)
def update_curso(
    id_curso: int,
    curso: CursoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar un curso"""
    db_curso = crud_curso.get_curso(db, id_curso)
    if not db_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    if current_user.rol != "ADMIN" and db_curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este curso"
        )
    
    updated_curso = crud_curso.update_curso(db, id_curso, curso)
    return updated_curso

@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un curso"""
    db_curso = crud_curso.get_curso(db, id_curso)
    if not db_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    if current_user.rol != "ADMIN" and db_curso.id_instructor != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este curso"
        )
    
    crud_curso.delete_curso(db, id_curso)
    return None

@router.get("/instructor/{id_instructor}", response_model=List[CursoResponse])
def get_cursos_by_instructor(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los cursos de un instructor"""
    return crud_curso.get_cursos_by_instructor(db, id_instructor)

@router.get("/area/{id_area}", response_model=List[CursoResponse])
def get_cursos_by_area(
    id_area: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los cursos de un área"""
    return crud_curso.get_cursos_by_area(db, id_area)