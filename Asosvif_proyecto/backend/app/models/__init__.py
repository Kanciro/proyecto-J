# Importar Base primero
from app.core.database import Base

# Importar modelos en orden de dependencias
from app.models.usuario import Usuario, RolEnum
from app.models.instructor import Instructor
from app.models.area import AreaHidroponia
from app.models.curso import Curso, NivelDificultad
from app.models.modulo import Modulo
from app.models.leccion import Leccion
from app.models.recurso import RecursoLeccion, TipoRecurso
from app.models.inscripcion import Inscripcion
from app.models.progreso import ProgresoLeccion
from app.models.calificacion import Calificacion
from app.models.mensaje import ComentarioMensaje

# Exportar todos los modelos
__all__ = [
    "Base",
    "Usuario",
    "RolEnum",
    "Instructor",
    "AreaHidroponia",
    "Curso",
    "NivelDificultad",
    "Modulo",
    "Leccion",
    "RecursoLeccion",
    "TipoRecurso",
    "Inscripcion",
    "ProgresoLeccion",
    "Calificacion",
    "ComentarioMensaje"
]