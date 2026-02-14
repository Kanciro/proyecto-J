import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/hidroponia")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "hidroponia")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta_super_segura_cambiala_123456789")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # App
    APP_NAME: str = os.getenv("APP_NAME", "Hidroponia API")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    API_V1_STR: str = "/api/v1"

settings = Settings()