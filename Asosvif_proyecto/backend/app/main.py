from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos los routers de tus carpetas
from routers.user_router import router as user_router
from routers.course_router import router as course_router

app = FastAPI()

# Configuración de CORS (La llave maestra)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectamos las rutas al servidor principal
app.include_router(user_router, prefix="/users", tags=["Usuarios"])
app.include_router(course_router, prefix="/courses", tags=["Cursos"])

@app.get("/")
def home():
    return {"status": "Servidor de Hidroponía Online"}