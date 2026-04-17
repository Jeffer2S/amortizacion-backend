from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Convertir DATABASE_URL a formato psycopg si es necesario
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

logger.info(f"📊 Conectando a base de datos: {database_url[:60]}...")

try:
    engine = create_engine(database_url, echo=False, pool_pre_ping=True)
    logger.info("✅ Conexión a base de datos exitosa")
except Exception as e:
    logger.error(f"❌ Error al conectar: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
