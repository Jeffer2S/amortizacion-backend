import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import auth, institution, credits, amortization, investments
from app.database import engine
from app.models import Base

app = FastAPI(
    title="Simulador de Amortización e Inversiones",
    description="API para simulación de tablas de amortización (francés/alemán) y DPF",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CREAR TABLAS AL INICIAR ───────────────────────────────────────
# Esto asegura que todas las tablas existan
Base.metadata.create_all(bind=engine)

# ── CORS ──────────────────────────────────────────────────────────
# CORS dinámico según el entorno
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# En producción, agrega tus dominios
if settings.environment == "production":
    cors_origins.extend([
        "https://tu-frontend.com",  # ← Reemplaza con tu dominio real
        "https://www.tu-frontend.com",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rutas estáticas para uploads ──────────────────────────────────
os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# ── Routers ───────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(institution.router)
app.include_router(credits.router)
app.include_router(amortization.router)
app.include_router(investments.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
