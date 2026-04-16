# Guía Completa de Despliegue en Railway

## 📋 Índice
1. [Requisitos Previos](#requisitos-previos)
2. [Paso 1: Preparar el Proyecto](#paso-1-preparar-el-proyecto)
3. [Paso 2: Configurar GitHub](#paso-2-configurar-github)
4. [Paso 3: Crear Cuenta en Railway](#paso-3-crear-cuenta-en-railway)
5. [Paso 4: Configurar Railway](#paso-4-configurar-railway)
6. [Paso 5: Variables de Entorno](#paso-5-variables-de-entorno)
7. [Paso 6: Desplegar](#paso-6-desplegar)
8. [Paso 7: Verificar Despliegue](#paso-7-verificar-despliegue)
9. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:
- ✅ Cuenta en GitHub (gratis)
- ✅ Cuenta en Railway (puedes crear una con GitHub)
- ✅ Git instalado en tu máquina
- ✅ Python 3.12 instalado localmente
- ✅ Tu proyecto en orden (que ya tienes)

---

## Paso 1: Preparar el Proyecto

### 1.1 Crear archivo `.env.example`
Este archivo documenta qué variables de entorno se necesitan (SIN valores secretos):

```bash
# Abre PowerShell en la carpeta del proyecto y crea el archivo:
```

Crea el archivo `c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend\.env.example` con:

```
DATABASE_URL=postgresql+psycopg://user:password@host:port/database
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOAD_DIR=./uploads
ENVIRONMENT=production
```

### 1.2 Actualizar `requirements.txt`
Asegúrate de que contiene TODAS las dependencias necesarias. El tuyo ya está bien, pero agrega esto al final si no está:

```txt
gunicorn==23.0.0
```

Gunicorn es el servidor que Railway usará en producción.

### 1.3 Crear archivo `Procfile`
Este archivo le dice a Railway cómo ejecutar tu aplicación.

Crea el archivo `c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend\Procfile` con:

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
```

**Explicación:**
- `web:` - Tipo de proceso (web server)
- `gunicorn` - Servidor WSGI
- `-w 4` - 4 workers (procesos)
- `-k uvicorn.workers.UvicornWorker` - Usa Uvicorn como worker
- `-b 0.0.0.0:$PORT` - Escucha en el puerto que Railway asigne
- `app.main:app` - Ruta a tu aplicación FastAPI

### 1.4 Actualizar `app/config.py`
Modifica tu archivo de configuración para soportar variables de entorno en producción:

**Archivo actual:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:password@localhost:5432/amortizaciones_db"
    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"

settings = Settings()
```

**Actualizar a:**
```python
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
    
    # Archivos
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Entorno
    environment: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### 1.5 Actualizar `app/main.py`
Modifica los CORS para soportar tu dominio en Railway:

**Actual:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Actualizar a:**
```python
import os

# CORS dinámico según el entorno
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# En producción, agrega tus dominios
if os.getenv("ENVIRONMENT") == "production":
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
```

### 1.6 Crear archivo `.dockerignore` (opcional pero recomendado)
Crea el archivo `c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend\.dockerignore`:

```
__pycache__
*.pyc
.git
.gitignore
.env
.venv
venv
.pytest_cache
.mypy_cache
.coverage
htmlcov
dist
build
*.egg-info
.DS_Store
.idea
.vscode
uploads/*
!uploads/.gitkeep
node_modules
```

---

## Paso 2: Configurar GitHub

### 2.1 Inicializar repositorio Git (si aún no está)
```powershell
cd c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend
git init
git config user.name "Tu Nombre"
git config user.email "tu.email@gmail.com"
```

### 2.2 Crear `.gitignore` (ya lo hiciste)
Verifica que tu `.gitignore` esté en la raíz del proyecto.

### 2.3 Agregar archivos y hacer commit
```powershell
git add .
git commit -m "Configuración inicial para despliegue en Railway"
```

### 2.4 Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre del repo: `simulador-amortizacion-backend`
3. Descripción: `Backend API para simulación de amortizaciones e inversiones`
4. Selecciona: **Private** (si quieres privado)
5. NO inicialices README (ya tienes archivos)
6. Haz clic en **Create repository**

### 2.5 Conectar tu repositorio local con GitHub
```powershell
git remote add origin https://github.com/TU_USUARIO/simulador-amortizacion-backend.git
git branch -M main
git push -u origin main
```

**Nota:** Si usas autenticación HTTPS, se te pedirá que crees un **Personal Access Token** en GitHub:
1. Ve a https://github.com/settings/tokens
2. Haz clic en **Generate new token (classic)**
3. Dale permisos: `repo`, `workflow`
4. Copia el token y úsalo como contraseña cuando Git lo pida

---

## Paso 3: Crear Cuenta en Railway

### 3.1 Acceder a Railway
1. Ve a https://railway.app
2. Haz clic en **Start Project**
3. Elige **Deploy from GitHub** (si tienes cuenta en GitHub, es lo más fácil)

### 3.2 Autorizar Railway en GitHub
1. Se te redirigirá a GitHub
2. Haz clic en **Authorize Railway**
3. Selecciona tu repositorio: `simulador-amortizacion-backend`
4. Haz clic en **Install & Authorize**

---

## Paso 4: Configurar Railway

### 4.1 Crear un nuevo proyecto en Railway
1. En el dashboard de Railway, haz clic en **New Project**
2. Selecciona **Deploy from GitHub repo**
3. Elige tu repositorio `simulador-amortizacion-backend`
4. Haz clic en **Deploy**

### 4.2 Esperar a que Railway detecte tu proyecto
Railway debería:
- ✅ Detectar que es un proyecto Python
- ✅ Leer `requirements.txt`
- ✅ Leer `Procfile`
- ✅ Construir la imagen

Si todo va bien, verás en los logs algo como:
```
Building...
Running pip install...
```

### 4.3 Agregar base de datos PostgreSQL
Railway puede proporcionar una base de datos PostgreSQL automáticamente:

1. En tu proyecto de Railway, haz clic en **+ Add**
2. Busca y selecciona **PostgreSQL**
3. Se creará automáticamente una instancia
4. Railway inyectará la variable `DATABASE_URL` automáticamente ✨

---

## Paso 5: Variables de Entorno

### 5.1 Configurar variables en Railway
En el dashboard de Railway:

1. Ve a tu aplicación (la que desplegaste)
2. Haz clic en la pestaña **Variables**
3. Agrega estas variables:

| Variable | Valor | Notas |
|----------|-------|-------|
| `SECRET_KEY` | *Genera una clave segura* | Ver nota abajo |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Tiempo de expiración del token |
| `ENVIRONMENT` | `production` | Para detectar que estamos en producción |
| `UPLOAD_DIR` | `/tmp/uploads` | Railway usa /tmp para archivos temporales |

**⚠️ IMPORTANTE:** La variable `DATABASE_URL` se crea automáticamente cuando agregas PostgreSQL.

### 5.2 Generar SECRET_KEY segura
En PowerShell:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia la salida y pégala como valor de `SECRET_KEY` en Railway.

### 5.3 Verificar que las variables están configuradas
En Railway, deberías ver algo como:
```
DATABASE_URL: postgresql+psycopg://...
SECRET_KEY: abc123...
ALGORITHM: HS256
ACCESS_TOKEN_EXPIRE_MINUTES: 60
ENVIRONMENT: production
UPLOAD_DIR: /tmp/uploads
```

---

## Paso 6: Desplegar

### 6.1 Despliegue automático (recomendado)
Una vez configurado, Railway despliega automáticamente cada vez que haces `git push` a `main`.

Para desplegar cambios:
```powershell
git add .
git commit -m "Descripción de cambios"
git push origin main
```

Railway verá el cambio y automáticamente:
1. Descargará el código actualizado
2. Instalará dependencias
3. Construirá la imagen
4. Desplegará el nuevo código

### 6.2 Ver logs de despliegue
En el dashboard de Railway:
1. Haz clic en tu aplicación
2. Ve a la pestaña **Logs**
3. Verás el progreso del build en tiempo real

---

## Paso 7: Verificar Despliegue

### 7.1 Obtener URL pública
En el dashboard de Railway:
1. Ve a tu aplicación (la que desplegaste)
2. En la pestaña **Settings**, busca **Domains**
3. Verás algo como: `simulador-amortizacion-backend-production.up.railway.app`

### 7.2 Verificar salud de la aplicación
En tu navegador o con curl:
```bash
curl https://simulador-amortizacion-backend-production.up.railway.app/api/health
```

Deberías recibir:
```json
{"status":"ok","version":"1.0.0"}
```

### 7.3 Acceder a la documentación interactiva
- Swagger UI: `https://tu-url.up.railway.app/api/docs`
- ReDoc: `https://tu-url.up.railway.app/api/redoc`

### 7.4 Probar endpoints
Usa Postman, Insomnia o curl:
```bash
# Ejemplo: Verificar salud
curl https://tu-url.up.railway.app/api/health

# Ejemplo: Login (si tienes endpoint de auth)
curl -X POST https://tu-url.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

---

## Paso 8: Migraciones de Base de Datos (Alembic)

### 8.1 Ejecutar migraciones en producción
Las migraciones deben ejecutarse antes de que la aplicación inicie.

**Opción 1: Desde el CLI de Railway (recomendado)**

1. Ve a https://railway.app/dashboard
2. Selecciona tu proyecto
3. En la esquina superior derecha, haz clic en **CLI**
4. Descarga e instala Railway CLI
5. En PowerShell, ejecuta:
```powershell
railway login
railway link  # Selecciona tu proyecto
railway run alembic upgrade head
```

**Opción 2: Agregar run release en Procfile**

Actualiza tu `Procfile` para ejecutar migraciones automáticamente:

```
release: alembic upgrade head
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
```

Con esto, cada vez que despliegues, Railway ejecutará `alembic upgrade head` antes de iniciar la aplicación.

### 8.2 Verificar que las migraciones se ejecutaron
En los logs de Railway, deberías ver:
```
Running release command: alembic upgrade head
INFO [alembic.runtime.migration] Context impl PostgresqlImpl with dialect postgresql
INFO [alembic.runtime.migration] Will assume transactional DDL is supported by the current dialect
INFO [alembic.migration] Running upgrade 1d36690de02c -> ...
```

---

## Paso 9: Conectar tu Frontend

Si tienes un frontend (probablemente en Vue con Vite en puerto 5173):

### 9.1 Actualizar URL base en tu frontend
En tu aplicación Vue/Vite, actualiza el cliente HTTP para apuntar a tu API en Railway:

```typescript
// Si usas axios o fetch
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000/api'

// En producción:
// VITE_API_URL=https://tu-url.up.railway.app/api
```

### 9.2 Agregar CORS en el backend
Ya actualizaste `app/main.py`, pero asegúrate de que incluya el dominio de tu frontend:

```python
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if os.getenv("ENVIRONMENT") == "production":
    cors_origins.extend([
        "https://tu-frontend.com",
    ])
```

---

## Solución de Problemas

### ❌ Error: "ModuleNotFoundError: No module named 'app'"

**Causa:** Railway no está ejecutando desde el directorio correcto.

**Solución:** Asegúrate de que tu `Procfile` apunta a `app.main:app` correctamente.

### ❌ Error: "database connection failed"

**Causa:** `DATABASE_URL` no está configurado o es incorrecto.

**Solución:**
1. En Railway, agrega PostgreSQL desde **+ Add**
2. Verifica que `DATABASE_URL` aparezca en la sección **Variables**
3. Reinicia la aplicación en Railway

### ❌ Error: "Permission denied: 'uploads'" o problemas con archivos

**Causa:** Railway usa un sistema de archivos efímero. Los archivos se pierden al reiniciar.

**Solución:**
1. Usa un servicio de almacenamiento externo (AWS S3, Cloudinary, etc.)
2. O configura: `UPLOAD_DIR=/tmp/uploads` (archivos temporales)

### ❌ Error 413: "Request entity too large"

**Causa:** Límite de tamaño de archivo.

**Solución:** En tu `Procfile`, aumenta el tamaño máximo:

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT --limit-request-fields 32000 --limit-request-field-size 0 app.main:app
```

### ❌ El build está muy lento o falla

**Causa:** Demasiadas dependencias o caché corrupto.

**Solución:**
1. En Railway, ve a **Settings**
2. Haz clic en **Clear build cache**
3. Desplega nuevamente

### ❌ CORS error cuando se conecta el frontend

**Causa:** El origen del frontend no está en la lista de CORS permitidos.

**Solución:**
1. Actualiza `app/main.py` con tu dominio de frontend
2. Haz `git push origin main`
3. Railway desplegará automáticamente

---

## Resumen de Checklist

Antes de desplegar en producción:

- [ ] ✅ Archivo `Procfile` creado
- [ ] ✅ `requirements.txt` actualizado con `gunicorn`
- [ ] ✅ `.env.example` creado (sin valores secretos)
- [ ] ✅ `.gitignore` configurado correctamente
- [ ] ✅ `app/config.py` actualizado para leer variables de entorno
- [ ] ✅ `app/main.py` actualizado con CORS dinámicos
- [ ] ✅ Repositorio en GitHub configurado
- [ ] ✅ Proyecto en Railway creado
- [ ] ✅ PostgreSQL agregado en Railway
- [ ] ✅ Variables de entorno configuradas en Railway
- [ ] ✅ `Procfile` incluye comando de migraciones (release)
- [ ] ✅ URL pública verificada
- [ ] ✅ `/api/health` responde correctamente
- [ ] ✅ Frontend conectado con CORS correcto

---

## Comandos Rápidos

```powershell
# Verificar que todo está en git
git status

# Ver logs locales
git log --oneline

# Desplegar cambios (después de commitear)
git push origin main

# Ver estado en Railway
railway status

# Ver logs de Railway
railway logs

# Ejecutar comando en Railway (ej: migraciones)
railway run alembic upgrade head
```

---

## Referencias Útiles

- 📖 [Documentación de Railway](https://docs.railway.app/)
- 📖 [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- 📖 [Documentación de Alembic](https://alembic.sqlalchemy.org/)
- 📖 [Documentación de Gunicorn](https://gunicorn.org/)
- 🔗 [GitHub Personal Access Token](https://github.com/settings/tokens)
- 🔗 [Railway Dashboard](https://railway.app/dashboard)

---

**Última actualización:** 16 de abril de 2026

Si tienes dudas, revisa los logs en Railway o contacta al soporte de Railway en https://railway.app/support

¡Éxito con tu despliegue! 🚀
