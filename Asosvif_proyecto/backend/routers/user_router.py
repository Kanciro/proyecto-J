# routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib
import uuid

# Importaciones de tu backend
from database import get_db
from models.user_models import Usuario, Instructor, UserRole
from schemas.user_schema import UserCreate, UserOut, UserLogin # Importamos el nuevo esquema

router = APIRouter(
    tags=["Usuarios"]
)

# --- ENDPOINT: REGISTRO ---
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario (Estudiante, Instructor o Admin).
    """
    # 1. Verificar si el email ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    
    # 2. Hashing de la Contraseña (SHA256)
    password_hash = hashlib.sha256(user_data.password.encode('utf-8')).hexdigest()
    
    # 3. Crear la instancia del nuevo usuario
    new_user = Usuario(
        id_usuario=uuid.uuid4(), 
        email=user_data.email,
        password_hash=password_hash,
        nombre_completo=user_data.nombre_completo,
        rol=user_data.rol
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # 4. Si es instructor, crear entrada en tabla instructores
        if new_user.rol == UserRole.INSTRUCTOR:
            new_instructor = Instructor(id_instructor=new_user.id_usuario)
            db.add(new_instructor)
            db.commit()
            
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

# --- ENDPOINT: LOGIN ---
@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Valida las credenciales y permite el acceso.
    """
    # 1. Buscar al usuario por email
    user = db.query(Usuario).filter(Usuario.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credenciales incorrectas (Usuario no encontrado)."
        )
    
    # 2. Verificar contraseña
    incoming_hash = hashlib.sha256(user_credentials.password.encode('utf-8')).hexdigest()
    if user.password_hash != incoming_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (Contraseña inválida)."
        )
    
    # 3. Respuesta exitosa para el Frontend (React)
    return {
        "message": "Login exitoso",
        "user": {
            "id": str(user.id_usuario),
            "nombre": user.nombre_completo,
            "rol": user.rol,
            "email": user.email
        }
    }

