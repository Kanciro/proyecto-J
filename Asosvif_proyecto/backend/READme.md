---

# 🌱 Plataforma de Cursos de Hidroponía - API REST

API REST desarrollada con FastAPI para una plataforma de cursos en línea especializada en hidroponía, similar a Platzi.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Modelos de Datos](#modelos-de-datos)
- [Autenticación](#autenticación)
- [Subida de Archivos](#subida-de-archivos)
- [Testing](#testing)
- [Contribución](#contribución)

## ✨ Características

- 🔐 **Autenticación JWT** - Sistema seguro de autenticación con tokens
- 👥 **Gestión de Usuarios** - Tres roles: Admin, Instructor, Estudiante
- 📚 **CRUD Completo de Cursos** - Gestión de cursos, módulos y lecciones
- 📊 **Sistema de Progreso** - Seguimiento del avance de los estudiantes
- ⭐ **Calificaciones** - Sistema de ratings para cursos
- 💬 **Mensajería** - Comentarios en lecciones y mensajes privados
- 🖼️ **Subida de Imágenes** - Sistema de almacenamiento de archivos
- 📱 **CORS Habilitado** - Listo para integrarse con frontend

## 🛠️ Tecnologías

- **Python 3.11+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **PyMySQL** - Conector MySQL
- **Pydantic** - Validación de datos
- **JWT (PyJWT)** - Autenticación con tokens
- **Uvicorn** - Servidor ASGI
- **MySQL** - Base de datos relacional

## 📦 Requisitos Previos

- Python 3.11 o superior
- MySQL 8.0+ (vía XAMPP o instalación independiente)
- pip (gestor de paquetes de Python)
- Git (opcional)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Asosvif_proyecto/backend
```

### 2. Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

#### Opción A: Usando XAMPP

1. Inicia XAMPP
2. Inicia Apache y MySQL
3. Abre phpMyAdmin: `http://localhost/phpmyadmin`
4. Crea una nueva base de datos llamada `hidroponia`
5. Importa el archivo SQL:

```sql
-- Ejecuta el script SQL proporcionado en /database/schema.sql
```

#### Opción B: MySQL independiente

```bash
mysql -u root -p
CREATE DATABASE hidroponia;
USE hidroponia;
SOURCE /ruta/al/schema.sql;
```

## ⚙️ Configuración

### 1. Crear archivo `.env`

Crea un archivo `.env` en la carpeta `backend/` con el siguiente contenido:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost:3306/hidroponia
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=hidroponia

# Security Configuration
SECRET_KEY=tu_clave_secreta_super_segura_cambiala_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application Configuration
APP_NAME=Hidroponia API
DEBUG=True
API_V1_STR=/api/v1
```

⚠️ **IMPORTANTE**: Cambia `SECRET_KEY` por una clave segura en producción. Puedes generar una con:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. Crear directorios de uploads

```bash
mkdir uploads
mkdir uploads/cursos
mkdir uploads/usuarios
mkdir uploads/lecciones
```

## 🏃 Ejecución

### Desarrollo

```bash
# Desde la carpeta backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O usando Python directamente:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceder a la documentación

Una vez iniciado el servidor:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   │
│   ├── api/                    # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencias (autenticación, DB)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Router principal
│   │       └── endpoints/
│   │           ├── auth.py     # Login, registro
│   │           ├── usuarios.py
│   │           ├── cursos.py
│   │           ├── modulos.py
│   │           ├── lecciones.py
│   │           ├── recursos.py
│   │           ├── inscripciones.py
│   │           ├── progreso.py
│   │           ├── calificaciones.py
│   │           ├── mensajes.py
│   │           ├── instructores.py
│   │           └── upload.py   # Subida de archivos
│   │
│   ├── core/                   # Configuración central
│   │   ├── __init__.py
│   │   ├── config.py           # Variables de entorno
│   │   ├── database.py         # Conexión a DB
│   │   └── security.py         # JWT, hashing
│   │
│   ├── crud/                   # Operaciones de base de datos
│   │   ├── __init__.py
│   │   ├── base.py             # CRUD genérico
│   │   ├── usuario.py
│   │   ├── curso.py
│   │   ├── leccion.py
│   │   ├── inscripcion.py
│   │   └── progreso.py
│   │
│   ├── models/                 # Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── curso.py
│   │   ├── modulo.py
│   │   ├── leccion.py
│   │   ├── recurso.py
│   │   ├── inscripcion.py
│   │   ├── progreso.py
│   │   ├── calificacion.py
│   │   └── mensaje.py
│   │
│   └── schemas/                # Schemas Pydantic (validación)
│       ├── __init__.py
│       ├── usuario.py
│       ├── token.py
│       ├── curso.py
│       ├── leccion.py
│       ├── inscripcion.py
│       └── progreso.py
│
├── uploads/                    # Archivos subidos
│   ├── cursos/
│   ├── usuarios/
│   └── lecciones/
│
├── .env                        # Variables de entorno
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/login-json` | Login con JSON | No |
| POST | `/api/v1/auth/refresh` | Refrescar token | Sí |
| GET | `/api/v1/auth/verify` | Verificar token | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/usuarios/me` | Usuario actual | Sí |
| PUT | `/api/v1/usuarios/me` | Actualizar perfil | Sí |
| GET | `/api/v1/usuarios/` | Listar usuarios | Admin |
| GET | `/api/v1/usuarios/{id}` | Obtener usuario | Sí |
| GET | `/api/v1/usuarios/rol/{rol}` | Usuarios por rol | Admin |

### Instructores

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/instructores/` | Crear instructor | Admin |
| GET | `/api/v1/instructores/{id}` | Obtener instructor | No |

### Cursos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cursos/` | Listar cursos | No |
| GET | `/api/v1/cursos/{id}` | Obtener curso | No |
| POST | `/api/v1/cursos/` | Crear curso | Instructor |
| PUT | `/api/v1/cursos/{id}` | Actualizar curso | Instructor |
| DELETE | `/api/v1/cursos/{id}` | Eliminar curso | Instructor |
| GET | `/api/v1/cursos/instructor/{id}` | Cursos de instructor | No |
| GET | `/api/v1/cursos/area/{id}` | Cursos por área | No |

### Módulos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/modulos/curso/{id}` | Módulos del curso | No |
| GET | `/api/v1/modulos/{id}` | Obtener módulo | No |
| POST | `/api/v1/modulos/` | Crear módulo | Instructor |
| PUT | `/api/v1/modulos/{id}` | Actualizar módulo | Instructor |
| DELETE | `/api/v1/modulos/{id}` | Eliminar módulo | Instructor |

### Lecciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/lecciones/modulo/{id}` | Lecciones del módulo | No |
| GET | `/api/v1/lecciones/{id}` | Obtener lección | No |
| POST | `/api/v1/lecciones/` | Crear lección | Instructor |
| PUT | `/api/v1/lecciones/{id}` | Actualizar lección | Instructor |
| DELETE | `/api/v1/lecciones/{id}` | Eliminar lección | Instructor |

### Recursos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/recursos/leccion/{id}` | Recursos de lección | No |
| GET | `/api/v1/recursos/{id}` | Obtener recurso | No |
| POST | `/api/v1/recursos/` | Crear recurso | Instructor |
| PUT | `/api/v1/recursos/{id}` | Actualizar recurso | Instructor |
| DELETE | `/api/v1/recursos/{id}` | Eliminar recurso | Instructor |

### Inscripciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/inscripciones/mis-cursos` | Mis inscripciones | Estudiante |
| POST | `/api/v1/inscripciones/` | Inscribirse | Estudiante |
| DELETE | `/api/v1/inscripciones/{id}` | Cancelar inscripción | Estudiante |
| GET | `/api/v1/inscripciones/verificar/{id}` | Verificar inscripción | Sí |

### Progreso

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/progreso/inscripcion/{id}` | Progreso de inscripción | Estudiante |
| POST | `/api/v1/progreso/completar/{id}` | Marcar completada | Estudiante |
| POST | `/api/v1/progreso/actualizar-vista/{id}` | Actualizar vista | Estudiante |
| GET | `/api/v1/progreso/resumen/{id}` | Resumen de progreso | Estudiante |

### Calificaciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/calificaciones/` | Calificar curso | Estudiante |
| GET | `/api/v1/calificaciones/curso/{id}` | Calificaciones del curso | No |
| GET | `/api/v1/calificaciones/mi-calificacion/{id}` | Mi calificación | Estudiante |

### Mensajes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/mensajes/` | Enviar mensaje | Sí |
| GET | `/api/v1/mensajes/leccion/{id}` | Comentarios de lección | Sí |
| GET | `/api/v1/mensajes/mis-mensajes` | Mis mensajes | Sí |
| GET | `/api/v1/mensajes/conversacion/{id}` | Conversación con usuario | Sí |
| DELETE | `/api/v1/mensajes/{id}` | Eliminar mensaje | Sí |

### Subida de Archivos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/upload/imagen/curso` | Subir imagen de curso | Instructor |
| POST | `/api/v1/upload/imagen/usuario` | Subir foto de perfil | Sí |
| POST | `/api/v1/upload/imagen/leccion` | Subir imagen de lección | Instructor |
| GET | `/api/v1/upload/imagen/cursos/{filename}` | Obtener imagen | No |
| GET | `/api/v1/upload/imagen/usuarios/{filename}` | Obtener imagen | No |
| GET | `/api/v1/upload/imagen/lecciones/{filename}` | Obtener imagen | No |
| DELETE | `/api/v1/upload/imagen/{tipo}/{filename}` | Eliminar imagen | Instructor |

## 📊 Modelos de Datos

### Usuario
```python
{
  "id_usuario": int,
  "email": str,
  "nombre_completo": str,
  "rol": "ADMIN" | "INSTRUCTOR" | "ESTUDIANTE",
  "fecha_creacion": datetime
}
```

### Curso
```python
{
  "id_curso": int,
  "id_instructor": int,
  "id_area": int,
  "titulo": str,
  "descripcion": str,
  "nivel_dificultad": "BASICO" | "INTERMEDIO" | "AVANZADO",
  "url_portada": str,
  "puntuacion_media": float,
  "fecha_publicacion": datetime
}
```

### Módulo
```python
{
  "id_modulo": int,
  "id_curso": int,
  "titulo_modulo": str,
  "orden": int
}
```

### Lección
```python
{
  "id_leccion": int,
  "id_modulo": int,
  "titulo_leccion": str,
  "orden": int,
  "descripcion_breve": str
}
```

### Recurso
```python
{
  "id_recurso": int,
  "id_leccion": int,
  "tipo_recurso": "VIDEO" | "TEXTO_ENRIQUECIDO" | "PDF" | "ENLACE_EXTERNO" | "CODIGO_ZIP",
  "titulo_recurso": str,
  "contenido_texto": str,
  "url_recurso": str,
  "orden": int
}
```

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens) para autenticación.

### Flujo de autenticación:

1. **Registro**: 
```bash
POST /api/v1/auth/register
{
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "nombre_completo": "Juan Pérez",
  "rol": "ESTUDIANTE"
}
```

2. **Login**:
```bash
POST /api/v1/auth/login
{
  "username": "usuario@ejemplo.com",  # OAuth2 requiere "username"
  "password": "password123"
}

# Respuesta:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

3. **Uso del token**:
```bash
# En headers de las peticiones:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Roles y permisos:

- **ADMIN**: Acceso total al sistema
- **INSTRUCTOR**: Crear y gestionar cursos, módulos y lecciones
- **ESTUDIANTE**: Inscribirse en cursos, ver contenido, calificar

## 🖼️ Subida de Archivos

### Subir imagen:

```bash
POST /api/v1/upload/imagen/curso
Content-Type: multipart/form-data

file: [archivo.jpg]
```

### Respuesta:
```json
{
  "filename": "20250214_153045_a1b2c3d4.jpg",
  "url": "http://localhost:8000/api/v1/upload/imagen/cursos/20250214_153045_a1b2c3d4.jpg",
  "message": "Imagen subida exitosamente"
}
```

### Restricciones:
- Formatos permitidos: PNG, JPG, JPEG, GIF, WEBP
- Tamaño máximo: 5MB

## 🧪 Testing

### Probar con Swagger UI:

1. Accede a http://localhost:8000/docs
2. Haz clic en "Authorize" 🔒
3. Ingresa tu token JWT
4. Prueba los endpoints

### Ejemplo de flujo completo:

```bash
# 1. Registrar usuario admin
POST /api/v1/auth/register
{
  "email": "admin@hidroponia.com",
  "nombre_completo": "Admin",
  "rol": "ADMIN",
  "password": "admin123"
}

# 2. Login
POST /api/v1/auth/login
username: admin@hidroponia.com
password: admin123

# 3. Crear instructor (copiar token del paso anterior)
POST /api/v1/instructores/
{
  "id_instructor": 1,
  "biografia": "Experto en hidroponía",
  "url_foto_perfil": "https://..."
}

# 4. Subir imagen para curso
POST /api/v1/upload/imagen/curso
file: [seleccionar imagen]

# 5. Crear curso con la URL de la imagen
POST /api/v1/cursos/
{
  "titulo": "Curso de NFT",
  "descripcion": "Aprende hidroponía NFT",
  "nivel_dificultad": "BASICO",
  "id_instructor": 1,
  "id_area": 1,
  "url_portada": "[URL del paso 4]"
}
```

## 📝 Datos de Prueba

### SQL para insertar datos iniciales:

```sql
USE hidroponia;

-- Áreas de hidroponía
INSERT INTO areas_hidroponia (nombre_area) VALUES 
('Sistemas NFT'),
('Cultivo Vertical'),
('Hidroponía Doméstica'),
('Cultivos Comerciales');

-- Los usuarios e instructores se crean desde la API
```

## 🐛 Solución de Problemas

### Error: "Cannot connect to database"
- Verifica que MySQL esté corriendo en XAMPP
- Verifica las credenciales en `.env`
- Asegúrate que la base de datos `hidroponia` exista

### Error: "Module not found"
- Activa el entorno virtual: `venv\Scripts\activate`
- Reinstala dependencias: `pip install -r requirements.txt`

### Error: "Port 8000 already in use"
- Cambia el puerto: `uvicorn app.main:app --port 8001`
- O mata el proceso: `taskkill /F /IM python.exe` (Windows)

### Error: "ENUM value not found"
- Asegúrate de usar valores sin tilde: `BASICO`, no `BÁSICO`
- Ejecuta el script SQL de corrección proporcionado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👥 Autores

- **Tu Nombre** - Desarrollo inicial

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- La comunidad de Python

---

**Desarrollado con ❤️ para ASOSVIF**