from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db
from app.models.mensaje import ComentarioMensaje
from app.crud import leccion as crud_leccion
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter()

class MensajeCreate(BaseModel):
    id_destinatario: Optional[int] = None
    id_leccion: Optional[int] = None
    contenido: str
    es_privado: bool = False

class MensajeResponse(BaseModel):
    id_mensaje: int
    id_remitente: int
    id_destinatario: Optional[int]
    id_leccion: Optional[int]
    contenido: str
    es_privado: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class MensajeConUsuarios(MensajeResponse):
    remitente_nombre: str
    destinatario_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=MensajeResponse, status_code=status.HTTP_201_CREATED)
def crear_mensaje(
    mensaje: MensajeCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear un nuevo mensaje o comentario"""
    # Validar que al menos haya un destinatario o una lección
    if not mensaje.id_destinatario and not mensaje.id_leccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar un destinatario o una lección"
        )
    
    # Si tiene id_leccion, verificar que existe
    if mensaje.id_leccion:
        leccion = crud_leccion.get_leccion(db, mensaje.id_leccion)
        if not leccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lección no encontrada"
            )
    
    # Si tiene destinatario, verificar que existe
    if mensaje.id_destinatario:
        from app.crud.usuario import get_usuario_by_id
        destinatario = get_usuario_by_id(db, mensaje.id_destinatario)
        if not destinatario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destinatario no encontrado"
            )
    
    db_mensaje = ComentarioMensaje(
        id_remitente=current_user.id_usuario,
        id_destinatario=mensaje.id_destinatario,
        id_leccion=mensaje.id_leccion,
        contenido=mensaje.contenido,
        es_privado=mensaje.es_privado
    )
    
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    
    return db_mensaje

@router.get("/leccion/{id_leccion}", response_model=List[MensajeConUsuarios])
def get_comentarios_leccion(
    id_leccion: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener todos los comentarios públicos de una lección"""
    mensajes = db.query(ComentarioMensaje).filter(
        ComentarioMensaje.id_leccion == id_leccion,
        ComentarioMensaje.es_privado == False
    ).order_by(ComentarioMensaje.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    # Enriquecer con nombres de usuarios
    result = []
    for msg in mensajes:
        msg_dict = {
            "id_mensaje": msg.id_mensaje,
            "id_remitente": msg.id_remitente,
            "id_destinatario": msg.id_destinatario,
            "id_leccion": msg.id_leccion,
            "contenido": msg.contenido,
            "es_privado": msg.es_privado,
            "fecha_creacion": msg.fecha_creacion,
            "remitente_nombre": msg.remitente.nombre_completo,
            "destinatario_nombre": msg.destinatario.nombre_completo if msg.destinatario else None
        }
        result.append(msg_dict)
    
    return result

@router.get("/mis-mensajes", response_model=List[MensajeConUsuarios])
def get_mis_mensajes(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener todos los mensajes privados del usuario actual"""
    mensajes = db.query(ComentarioMensaje).filter(
        (ComentarioMensaje.id_remitente == current_user.id_usuario) |
        (ComentarioMensaje.id_destinatario == current_user.id_usuario),
        ComentarioMensaje.es_privado == True
    ).order_by(ComentarioMensaje.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    result = []
    for msg in mensajes:
        msg_dict = {
            "id_mensaje": msg.id_mensaje,
            "id_remitente": msg.id_remitente,
            "id_destinatario": msg.id_destinatario,
            "id_leccion": msg.id_leccion,
            "contenido": msg.contenido,
            "es_privado": msg.es_privado,
            "fecha_creacion": msg.fecha_creacion,
            "remitente_nombre": msg.remitente.nombre_completo,
            "destinatario_nombre": msg.destinatario.nombre_completo if msg.destinatario else None
        }
        result.append(msg_dict)
    
    return result

@router.get("/conversacion/{id_usuario}", response_model=List[MensajeConUsuarios])
def get_conversacion(
    id_usuario: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener conversación entre el usuario actual y otro usuario"""
    mensajes = db.query(ComentarioMensaje).filter(
        (
            (ComentarioMensaje.id_remitente == current_user.id_usuario) &
            (ComentarioMensaje.id_destinatario == id_usuario)
        ) |
        (
            (ComentarioMensaje.id_remitente == id_usuario) &
            (ComentarioMensaje.id_destinatario == current_user.id_usuario)
        ),
        ComentarioMensaje.es_privado == True
    ).order_by(ComentarioMensaje.fecha_creacion.asc()).offset(skip).limit(limit).all()
    
    result = []
    for msg in mensajes:
        msg_dict = {
            "id_mensaje": msg.id_mensaje,
            "id_remitente": msg.id_remitente,
            "id_destinatario": msg.id_destinatario,
            "id_leccion": msg.id_leccion,
            "contenido": msg.contenido,
            "es_privado": msg.es_privado,
            "fecha_creacion": msg.fecha_creacion,
            "remitente_nombre": msg.remitente.nombre_completo,
            "destinatario_nombre": msg.destinatario.nombre_completo if msg.destinatario else None
        }
        result.append(msg_dict)
    
    return result

@router.delete("/{id_mensaje}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mensaje(
    id_mensaje: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar un mensaje (solo el remitente o admin)"""
    mensaje = db.query(ComentarioMensaje).filter(
        ComentarioMensaje.id_mensaje == id_mensaje
    ).first()
    
    if not mensaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensaje no encontrado"
        )
    
    if current_user.rol != "ADMIN" and mensaje.id_remitente != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este mensaje"
        )
    
    db.delete(mensaje)
    db.commit()
    
    return None