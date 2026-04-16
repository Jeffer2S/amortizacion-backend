# COMANDOS EXACTOS PARA RAILWAY

**Copia y pega estos comandos exactamente en PowerShell**

---

## FASE 1: CONFIGURAR GIT (Local)

```powershell
# Abre PowerShell y entra a la carpeta del proyecto
cd c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend

# Inicializa Git (si no está ya inicializado)
git init

# Configura tu usuario
git config user.name "Tu Nombre Completo"
git config user.email "tu.email@gmail.com"

# Verifica que está bien
git config --list
```

---

## FASE 2: AGREGAR ARCHIVOS Y HACER COMMIT

```powershell
# Ver qué archivos hay
git status

# Agregar todos los archivos
git add .

# Hacer primer commit
git commit -m "Configuración inicial para despliegue en Railway"

# Verificar que se agregó
git log --oneline
```

---

## FASE 3: CONECTAR CON GITHUB (primero crea el repo en https://github.com/new)

```powershell
# Reemplaza TU_USUARIO con tu nombre de usuario en GitHub
git remote add origin https://github.com/TU_USUARIO/simulador-amortizacion-backend.git

# Cambia el nombre de la rama a main
git branch -M main

# Sube todo a GitHub
git push -u origin main

# Verifica que se subió
git remote -v
```

**Si pide contraseña:** GitHub pedirá un "Personal Access Token"
- Ve a https://github.com/settings/tokens
- Crea uno nuevo con permisos `repo` y `workflow`
- Copia el token
- Pégalo cuando Git lo pida

---

## FASE 4: VERIFICAR EN GITHUB

Abre tu navegador y ve a:
```
https://github.com/TU_USUARIO/simulador-amortizacion-backend
```

Deberías ver todos tus archivos ✓

---

## FASE 5: DESPLEGAR EN RAILWAY

```powershell
# 1. Ve a https://railway.app
# 2. Haz clic en "Start Project"
# 3. Haz clic en "Deploy from GitHub repo"
# 4. Autoriza Railway con GitHub
# 5. Selecciona tu repositorio "simulador-amortizacion-backend"
# 6. Haz clic en "Deploy Now"

# Espera a que Railway construya (ver logs en el dashboard)
```

---

## FASE 6: AGREGAR PostgreSQL EN RAILWAY

En el dashboard de Railway:

```
1. Ve a tu aplicación (la que desplegaste)
2. Haz clic en "+ Add"
3. Busca "PostgreSQL"
4. Haz clic en PostgreSQL
5. Espera a que se agregue
6. Railway automáticamente inyectará DATABASE_URL
```

---

## FASE 7: AGREGAR VARIABLES DE ENTORNO EN RAILWAY

En el dashboard de Railway, ve a tu aplicación → pestaña "Variables"

Copia y pega estas variables (una por una):

### Variable 1: SECRET_KEY
Primero, genera una clave segura. Abre PowerShell y ejecuta:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia la salida (algo como: `abc123xyz789...`)

En Railway, agrega:
- Key: `SECRET_KEY`
- Value: `[pega aquí la salida anterior]`

### Variable 2: ALGORITHM
- Key: `ALGORITHM`
- Value: `HS256`

### Variable 3: ACCESS_TOKEN_EXPIRE_MINUTES
- Key: `ACCESS_TOKEN_EXPIRE_MINUTES`
- Value: `60`

### Variable 4: ENVIRONMENT
- Key: `ENVIRONMENT`
- Value: `production`

### Variable 5: UPLOAD_DIR
- Key: `UPLOAD_DIR`
- Value: `/tmp/uploads`

**IMPORTANTE:** `DATABASE_URL` debe estar automáticamente (creado por PostgreSQL)

---

## FASE 8: VERIFICAR QUE TODO FUNCIONA

Abre PowerShell:

```powershell
# Obtén la URL de tu aplicación de Railway
# (algo como: simulador-amortizacion-backend-production.up.railway.app)

# Prueba el endpoint de salud
curl https://tu-url.up.railway.app/api/health

# Deberías recibir:
# {"status":"ok","version":"1.0.0"}
```

Si todo funciona, ¡tu backend está en vivo! 🎉

---

## FASE 9: DESPLEGAR CAMBIOS FUTUROS

Cada vez que hagas cambios, simplemente:

```powershell
# 1. Ve a tu carpeta
cd c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend

# 2. Agregar cambios
git add .

# 3. Commit
git commit -m "Descripción del cambio"

# 4. Push
git push origin main

# ¡Listo! Railway automáticamente:
# - Ve el cambio
# - Descarga el código
# - Instala dependencias
# - Construye
# - Desplega
```

---

## COMANDOS ÚTILES DURANTE EL PROCESO

```powershell
# Ver estado de Git
git status

# Ver cambios no subidos
git log --oneline -5

# Ver remoto configurado
git remote -v

# Deshacer último commit (CUIDADO)
git reset --soft HEAD~1

# Ver la URL de tu app en Railway (después de desplegar)
# (ve al dashboard de Railway, aplicación, pestaña "Settings")
```

---

## VERIFICAR MIGRACIONES (opcional, si usas Alembic)

Si necesitas ejecutar migraciones en Railway:

```powershell
# 1. Instala Railway CLI
# (descárgalo desde https://railway.app/cli)

# 2. Inicia sesión
railway login

# 3. Vincula tu proyecto
railway link

# 4. Ejecuta migraciones
railway run alembic upgrade head

# 5. Ver logs
railway logs
```

---

## URLS FINALES

Después de todo esto, tendrás:

```
Frontend (Vite):
http://localhost:5173 (desarrollo)
https://tu-frontend.com (producción)

Backend (FastAPI en Railway):
https://tu-url.up.railway.app/api/health (salud)
https://tu-url.up.railway.app/api/docs (documentación interactiva)
https://tu-url.up.railway.app/api/redoc (documentación ReDoc)

Base de datos (PostgreSQL en Railway):
postgresql://user:pass@rail.internal:5432/railway (automático)
```

---

## PROBLEMAS Y SOLUCIONES

### "git: not found" o "git is not installed"
**Solución:** Instala Git desde https://git-scm.com/download/win

### "python: not found" o "python is not installed"
**Solución:** Instala Python desde https://python.org

### "fatal: not a git repository"
**Solución:** Asegúrate de estar en la carpeta correcta y de haber ejecutado `git init`

### Railway no detecta el Procfile
**Solución:** Verifica que el archivo se llame exactamente `Procfile` (sin extensión) y esté en la raíz del proyecto

### Error "ModuleNotFoundError: No module named 'app'"
**Solución:** Revisa que tu `Procfile` tenga: `web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app`

### Base de datos no conecta
**Solución:** Agrega PostgreSQL en Railway (Fase 6)

### CORS error desde el frontend
**Solución:** En `app/main.py`, actualiza los `cors_origins` con tu dominio, luego `git push origin main`

---

## ARCHIVOS QUE DEBES TENER

Antes de desplegar, verifica que existen estos archivos en tu carpeta:

```
✓ Procfile
✓ requirements.txt (con gunicorn)
✓ .env.example
✓ .gitignore
✓ .dockerignore
✓ app/config.py (actualizado)
✓ app/main.py (con CORS dinámicos)
✓ alembic/ (carpeta completa)
✓ alembic.ini
✓ docker-compose.yml
```

---

**¡Listo! Síguelos en orden y tu app estará en vivo en 15 minutos.** 🚀
