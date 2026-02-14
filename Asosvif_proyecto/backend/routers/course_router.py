from fastapi import APIRouter

# Definimos el router que main.py está buscando
router = APIRouter()

@router.get("/cursos")
def listar_cursos():
    return {"message": "Aquí se mostrarán los cursos de hidroponía pronto"}