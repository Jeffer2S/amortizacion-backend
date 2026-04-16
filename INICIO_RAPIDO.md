# 🚀 GUÍA RÁPIDA - DESPLEGAR EN RAILWAY EN 15 MINUTOS

**¿Tienes prisa? Este es tu archivo.** 

---

## 📚 Elige tu camino:

### 🟢 OPCIÓN 1: Solo quiero desplegar (sin entender mucho)
**Archivo:** `COMANDOS_RAILWAY.md`
- Copia y pega comandos
- 6 fases claras
- Tiempo: 5-10 minutos

### 🟡 OPCIÓN 2: Quiero entender los pasos
**Archivo:** `RAILWAY_PASOS_EXACTOS.md`
- Pasos explicados
- Checklist
- Solución de problemas rápidos
- Tiempo: 10-15 minutos

### 🔴 OPCIÓN 3: Quiero todo (para expertos)
**Archivo:** `DEPLOYMENT_RAILWAY_GUIDE.md`
- Guía completa
- Teoría incluida
- Troubleshooting exhaustivo
- Tiempo: 30-45 minutos

---

## ⚡ DESPLIEGUE EXPRÉS (5 MINUTOS)

Si tienes prisa, aquí va:

### 1️⃣ Git setup (PowerShell)
```powershell
cd c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
git add .
git commit -m "Initial Railway setup"
```

### 2️⃣ GitHub
```powershell
# Crea repo en https://github.com/new (privado, sin README)
# Entonces ejecuta:
git remote add origin https://github.com/TU_USER/simulador-amortizacion-backend.git
git branch -M main
git push -u origin main
```

### 3️⃣ Railway
1. Ve a https://railway.app
2. "Start Project" → "Deploy from GitHub repo"
3. Autoriza y selecciona tu repo
4. Espera el build (5 minutos)

### 4️⃣ Variables (en Railway Dashboard)
```
DATABASE_URL → [automático con PostgreSQL]
SECRET_KEY → [ejecuta: python -c "import secrets; print(secrets.token_urlsafe(32))"]
ALGORITHM → HS256
ACCESS_TOKEN_EXPIRE_MINUTES → 60
ENVIRONMENT → production
UPLOAD_DIR → /tmp/uploads
```

### 5️⃣ Verificar
```powershell
# Espera 2 minutos, luego:
curl https://[tu-url].up.railway.app/api/health
# Deberías recibir: {"status":"ok","version":"1.0.0"}
```

**¡Listo! Tu API está en vivo.** 🎉

---

## 📁 ARCHIVOS CREADOS PARA TI

| Archivo | Propósito | Lee si... |
|---------|-----------|-----------|
| `Procfile` | Configuración de servidor | Lo necesita Railway |
| `.env.example` | Variables de entorno documentadas | Necesitas saber qué variables |
| `.dockerignore` | Excluir archivos del build | Configuración avanzada |
| `COMANDOS_RAILWAY.md` | Comandos exactos para copiar | Tienes prisa (5 min) |
| `RAILWAY_PASOS_EXACTOS.md` | Pasos claros y ejecutivos | Necesitas entender (15 min) |
| `DEPLOYMENT_RAILWAY_GUIDE.md` | Guía completa y detallada | Quieres TODO (45 min) |
| `RESUMEN_CAMBIOS.md` | Qué se cambió en tu proyecto | Curiosidad técnica |

---

## ✅ VERIFICACIÓN RÁPIDA

Antes de desplegar, verifica que tienes:

```
✓ Procfile                          ← Nuevo
✓ .env.example                      ← Nuevo
✓ .dockerignore                     ← Nuevo
✓ .gitignore                        ← Ya existe
✓ requirements.txt (con gunicorn)   ← Actualizado
✓ app/config.py (con variables)     ← Actualizado
✓ app/main.py (con CORS dinámicos)  ← Actualizado
✓ alembic/                          ← Sin cambios
✓ Repositorio en GitHub             ← Necesitas crear
```

---

## 🆘 PROBLEMAS TÍPICOS

| Problema | Solución |
|----------|----------|
| "git: not found" | Instala Git: https://git-scm.com/download/win |
| "python: not found" | Instala Python: https://python.org |
| Railway no ve el Procfile | Verifica que esté en la raíz (sin carpeta) |
| Base de datos no conecta | Agrega PostgreSQL en Railway ("+Add") |
| CORS error | Actualiza `cors_origins` en `app/main.py` con tu dominio |
| Migraciones no se ejecutan | El `Procfile` debe tener `release: alembic upgrade head` |

---

## 🎯 MI RECOMENDACIÓN

1. **HOY:** Lee `COMANDOS_RAILWAY.md` (5 min) y desplega
2. **DESPUÉS:** Lee `RAILWAY_PASOS_EXACTOS.md` (10 min) para entender mejor
3. **SI TIENES PROBLEMAS:** Abre `DEPLOYMENT_RAILWAY_GUIDE.md` (30 min)

---

## 📞 CONTACTOS

- 🎓 Documentación Railway: https://docs.railway.app/
- 🆘 Soporte Railway: https://railway.app/support
- 📖 FastAPI: https://fastapi.tiangolo.com/
- 🔐 GitHub: https://github.com/settings/tokens

---

## 🚀 ¡COMIENZA AQUÍ!

Abre este archivo: **`COMANDOS_RAILWAY.md`**

Y copia los comandos paso a paso. En 10 minutos estarás en vivo.

---

**¡Buena suerte! Tu backend estará en Railway antes de que termines el café.** ☕
