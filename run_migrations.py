#!/usr/bin/env python
"""Script para ejecutar migraciones manualmente"""
import os
import sys
from alembic.config import Config
from alembic import command

# Configurar la ruta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Leer DATABASE_URL desde environment o .env
from app.config import settings

# Configurar Alembic
cfg = Config('alembic.ini')
cfg.set_main_option('sqlalchemy.url', settings.database_url)

# Ejecutar upgrade
print(f"🔄 Ejecutando migraciones...")
print(f"📊 Base de datos: {settings.database_url[:50]}...")

try:
    command.upgrade(cfg, 'head')
    print("✅ ¡Migraciones ejecutadas exitosamente!")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
