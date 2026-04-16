# ⚡ RESUMEN EJECUTIVO - Despliegue en Railway

**Fecha:** 16 de abril de 2026  
**Estado:** Configuración completada ✅

---

## 🚀 PASOS EXACTOS (paso a paso)

### PASO 1: Preparar el código (LOCAL)
```powershell
# 1.1 Abre PowerShell en tu carpeta del backend
cd c:\Users\js\Documents\Octavo\economia\codigo\amortizacion\backend

# 1.2 Verifica que tienes estos 5 archivos creados:
# - Procfile (servidor)
# - .env.example (documentación de variables)
# - .gitignore (qué no subir a Git)
# - .dockerignore (qué no incluir en Docker)
# - requirements.txt (actualizado con gunicorn)

# 1.3 Configura Git (primera vez)
git init
git config user.name "Tu Nombre"
git config user.email "tu.email@gmail.com"

# 1.4 Agrega todos los archivos
git add .
git commit -m "Configuración inicial para Railway"
```

### PASO 2: Crear repositorio en GitHub
```powershell
# 2.1 En el navegador:
# - Ve a https://github.com/new
# - Nombre: simulador-amortizacion-backend
# - Descripción: Backend API para amortizaciones
# - Privado (recomendado)
# - NO inicialices README
# - Crea el repo

# 2.2 Conecta tu repositorio local
git remote add origin https://github.com/TU_USUARIO/simulador-amortizacion-backend.git
git branch -M main
git push -u origin main

# (Sigue las instrucciones de GitHub si te pide token)
```

### PASO 3: Crear cuenta en Railway y desplegar
```
1. Ve a https://railway.app
2. Haz clic en "Start Project"
3. Elige "Deploy from GitHub repo"
4. Autoriza Railway con tu cuenta de GitHub
5. Selecciona tu repositorio
6. Railway automáticamente:
   ✓ Detectará que es Python
   ✓ Leerá requirements.txt
   ✓ Leerá Procfile
   ✓ Comenzará el despliegue
```

### PASO 4: Agregar base de datos PostgreSQL en Railway
```
1. En el dashboard de Railway, ve a tu app
2. Haz clic en "+ Add"
3. Busca "PostgreSQL"
4. Haz clic para agregar
5. Railway crea automáticamente la BD
6. Railway inyecta DATABASE_URL automáticamente ✨
```

### PASO 5: Configurar variables de entorno en Railway
En el dashboard de Railway, ve a tu aplicación y haz clic en "Variables".

Agrega estas 5 variables:

```
SECRET_KEY = [Ejecuta esto en PowerShell: python -c "import secrets; print(secrets.token_urlsafe(32))"]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ENVIRONMENT = production
UPLOAD_DIR = /tmp/uploads
```

**IMPORTANTE:** `DATABASE_URL` se crea automáticamente con PostgreSQL.

### PASO 6: Verificar despliegue
```bash
# El despliegue está listo cuando:

# 1. Ve a tu URL en Railway (algo como: app-name-production.up.railway.app)
# 2. Prueba el endpoint de salud:
curl https://tu-url.up.railway.app/api/health

# 3. Deberías ver:
{"status":"ok","version":"1.0.0"}

# 4. Accede a la documentación interactiva:
https://tu-url.up.railway.app/api/docs
```

---

## 📋 CHECKLIST FINAL

Antes de desplegar a producción, verifica:

- [ ] ✅ Archivo `Procfile` existe en la raíz
- [ ] ✅ `requirements.txt` tiene `gunicorn==23.0.0`
- [ ] ✅ `.env.example` documentado (sin valores secretos)
- [ ] ✅ `.gitignore` configurado
- [ ] ✅ `app/config.py` lee variables de entorno
- [ ] ✅ `app/main.py` tiene CORS dinámicos
- [ ] ✅ Código en GitHub (rama `main`)
- [ ] ✅ Proyecto creado en Railway
- [ ] ✅ PostgreSQL agregado en Railway
- [ ] ✅ Variables de entorno configuradas en Railway
- [ ] ✅ `/api/health` responde correctamente
- [ ] ✅ Documentación accesible en `/api/docs`

---

## 🔄 DESPLIEGUES FUTUROS

Para desplegar cambios en el futuro:

```powershell
# 1. Haz cambios en tu código
# (editar archivos, agregar funcionalidad, etc.)

# 2. Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# ¡Listo! Railway automáticamente:
# - Detecta el cambio
# - Descarga el código
# - Instala dependencias
# - Construye la app
# - Desplega
```

---

## 🆘 PROBLEMAS COMUNES

### Problema: "ModuleNotFoundError: No module named 'app'"
**Solución:** Verifica que `Procfile` tenga: `web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app`

### Problema: Error de conexión a base de datos
**Solución:** 
1. Agrega PostgreSQL en Railway (Paso 4)
2. Verifica que `DATABASE_URL` aparezca en Variables
3. Reinicia la app

### Problema: Error CORS desde el frontend
**Solución:** En `app/main.py`, actualiza `cors_origins` con tu dominio de frontend:
```python
cors_origins.extend([
    "https://tu-frontend.com",
])
```
Luego `git push origin main`

### Problema: Error 413 - Archivo muy grande
**Solución:** En `Procfile`, cambia el comando web a:
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT --limit-request-fields 32000 --limit-request-field-size 0 app.main:app
```

### Problema: El build es muy lento
**Solución:** En Railway → Settings → Clear build cache → Redeploy

---

## 📱 URL PÚBLICA

Después de desplegar, tu URL será:
```
https://simulador-amortizacion-backend-production.up.railway.app
```

(Railway generará un nombre único)

---

## 🔐 SEGURIDAD

**IMPORTANTE:**
- ✅ NUNCA hagas push de `.env` a GitHub
- ✅ El `SECRET_KEY` está oculto en Railway (no visible)
- ✅ Las migraciones se ejecutan automáticamente
- ✅ Las credenciales de BD están inyectadas por Railway

---

## 📞 SOPORTE

- 📖 Documentación Railway: https://docs.railway.app/
- 🆘 Soporte Railway: https://railway.app/support
- 📖 FastAPI: https://fastapi.tiangolo.com/
- 🔗 Mi repositorio: https://github.com/TU_USUARIO/simulador-amortizacion-backend

---

**¿Listo para desplegar? ¡Comienza con el PASO 1!** 🚀
