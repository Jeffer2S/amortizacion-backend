#!/usr/bin/env python
"""Script para ejecutar migraciones manualmente"""
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from alembic.config import Config
    from alembic import command
    from app.config import settings
    
    logger.info("🔄 Iniciando migraciones...")
    logger.info(f"📊 Base de datos configurada")
    
    # Asegurarse de que DATABASE_URL esté configurado
    if not settings.database_url:
        logger.error("❌ ERROR: DATABASE_URL no está configurado")
        sys.exit(1)
    
    # Convertir a formato psycopg si es necesario
    db_url = settings.database_url
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    logger.info(f"📍 Conectando a: {db_url[:60]}...")
    
    # Configurar Alembic
    cfg = Config('alembic.ini')
    cfg.set_main_option('sqlalchemy.url', db_url)
    
    # Ejecutar upgrade
    logger.info("⏳ Ejecutando: alembic upgrade head...")
    command.upgrade(cfg, 'head')
    logger.info("✅ ¡Migraciones completadas exitosamente!")
    
except ImportError as e:
    logger.error(f"❌ Error de importación: {e}")
    logger.error("Asegúrate de que alembic está instalado en requirements.txt")
    sys.exit(1)
except Exception as e:
    logger.error(f"❌ Error durante migraciones: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
