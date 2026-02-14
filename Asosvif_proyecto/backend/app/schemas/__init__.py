from app.schemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioInDB,
    UsuarioLogin
)
from app.schemas.token import Token, TokenData
from app.schemas.curso import (
    CursoBase,
    CursoCreate,
    CursoUpdate,
    CursoResponse,
    CursoConModulos
)
from app.schemas.modulo import (
    ModuloBase,
    ModuloCreate,
    ModuloUpdate,
    ModuloResponse,
    ModuloConLecciones
)
from app.schemas.leccion import (
    LeccionBase,
    LeccionCreate,
    LeccionUpdate,
    LeccionResponse,
    LeccionConRecursos
)
from app.schemas.recurso import (
    RecursoBase,
    RecursoCreate,
    RecursoUpdate,
    RecursoResponse
)
from app.schemas.inscripcion import (
    InscripcionBase,
    InscripcionCreate,
    InscripcionResponse
)
from app.schemas.progreso import (
    ProgresoBase,
    ProgresoCreate,
    ProgresoUpdate,
    ProgresoResponse,
    ProgresoResumen
)