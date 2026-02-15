from sqlalchemy.orm import Session
from app.models.usuario import Usuario, RolEnum
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from typing import Optional, List


class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):
    """CRUD operations para Usuario"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_id(self, db: Session, *, id_usuario: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    def create(self, db: Session, *, obj_in: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        hashed_password = get_password_hash(obj_in.password)
        db_obj = Usuario(
            email=obj_in.email,
            password_hash=hashed_password,
            nombre_completo=obj_in.nombre_completo,
            rol=obj_in.rol
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: Usuario, obj_in: UsuarioUpdate
    ) -> Usuario:
        """Actualizar usuario"""
        update_data = obj_in.dict(exclude_unset=True)
        
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password_hash"] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        usuario = self.get_by_email(db, email=email)
        if not usuario:
            return None
        if not verify_password(password, usuario.password_hash):
            return None
        return usuario
    
    def is_active(self, usuario: Usuario) -> bool:
        """Verificar si el usuario está activo"""
        return True  # Por ahora todos los usuarios están activos
    
    def is_admin(self, usuario: Usuario) -> bool:
        """Verificar si el usuario es admin"""
        return usuario.rol == RolEnum.ADMIN
    
    def is_instructor(self, usuario: Usuario) -> bool:
        """Verificar si el usuario es instructor"""
        return usuario.rol == RolEnum.INSTRUCTOR
    
    def is_estudiante(self, usuario: Usuario) -> bool:
        """Verificar si el usuario es estudiante"""
        return usuario.rol == RolEnum.ESTUDIANTE
    
    def get_multi_by_rol(
        self, db: Session, *, rol: RolEnum, skip: int = 0, limit: int = 100
    ) -> List[Usuario]:
        """Obtener usuarios por rol"""
        return (
            db.query(Usuario)
            .filter(Usuario.rol == rol)
            .offset(skip)
            .limit(limit)
            .all()
        )


# Instancia del CRUD para usuarios
usuario = CRUDUsuario(Usuario)

# Funciones helper para mantener compatibilidad con código anterior
def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    return usuario.get_by_email(db, email=email)

def get_usuario_by_id(db: Session, id_usuario: int) -> Optional[Usuario]:
    return usuario.get_by_id(db, id_usuario=id_usuario)

def create_usuario(db: Session, usuario_in: UsuarioCreate) -> Usuario:
    return usuario.create(db, obj_in=usuario_in)

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    return usuario.get_multi(db, skip=skip, limit=limit)

def update_usuario(db: Session, db_obj: Usuario, usuario_in: UsuarioUpdate) -> Usuario:
    return usuario.update(db, db_obj=db_obj, obj_in=usuario_in)

def authenticate_usuario(db: Session, email: str, password: str) -> Optional[Usuario]:
    return usuario.authenticate(db, email=email, password=password)