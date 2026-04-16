import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import auth, institution, credits, amortization, investments

app = FastAPI(
    title="Simulador de Amortización e Inversiones",
    description="API para simulación de tablas de amortización (francés/alemán) y DPF",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
