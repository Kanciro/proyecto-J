from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 1. Cargar variables de entorno
load_dotenv()

# 2. Definir la URL de la base de datos (puedes usar os.getenv("DATABASE_URL") si está en el .env)
DATABASE_URL = "sqlite:///./test.db"

# 3. Crear el motor (Engine) - ¡Esto faltaba!
# El argumento "check_same_thread" es necesario solo para SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 4. Configurar la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Clase base para los modelos
Base = declarative_base()

# 6. Generador de sesiones para los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()