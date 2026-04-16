from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Base de datos
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:password@localhost:5432/amortizaciones_db"
    )
    
    # Seguridad
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Almacenamiento
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Entorno
    environment: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
