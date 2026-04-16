# 💻 COMANDOS EXACTOS A EJECUTAR

## Terminal 1: Iniciar PostgreSQL

```powershell
# Desde la RAÍZ del proyecto
docker-compose up -d

# Esperar 15-20 segundos...

# Verificar
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE          STATUS
670dc0293c34   postgres:16    Up 20 seconds (healthy)   amortizaciones_db
```

---

## Terminal 2: Configurar Backend

### Paso 1: Entrar a la carpeta backend
```powershell
cd backend
```

### Paso 2: Crear entorno virtual (solo la primera vez)
```powershell
python -m venv venv
```

### Paso 3: Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

**Expected:** El prompt debe cambiar a:
```powershell
(venv) PS C:\Users\js\...\backend>
```

### Paso 4: Instalar dependencias
```powershell
pip install -r requirements.txt
```

**Expected:** Instala 45+ paquetes

### Paso 5: Aplicar migraciones
```powershell
alembic upgrade head
```

**Expected:**
```
INFO [alembic.runtime.migration] Running upgrade  -> 1d36690de02c, initial_schema
```

### Paso 6: Iniciar servidor
```powershell
uvicorn app.main:app --reload --port 8000
```

**Expected:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## ✅ Verificar que Todo Funciona

### En Terminal 3: Probar API

```powershell
# Health check
Invoke-WebRequest http://localhost:8000/api/health

# Expected response:
# {"status":"ok","version":"1.0.0"}
```

### O directamente en navegador:
- http://localhost:8000/api/docs (Swagger)
- http://localhost:8000/api/health (Health check)

---

## 🔄 Resumen Visual

```
Terminal 1:
    docker-compose up -d
    ↓ Esperar 20s
    docker ps (verificar)

Terminal 2:
    cd backend
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    alembic upgrade head
    uvicorn app.main:app --reload --port 8000
    ↓
    Backend está listo en http://localhost:8000

Terminal 3:
    Invoke-WebRequest http://localhost:8000/api/health
    ↓
    {"status":"ok"} ✓
```

---

## ⏱️ Tiempo Estimado

| Paso | Duración |
|------|----------|
| docker-compose up | 20-30s |
| pip install | 2-3 min |
| alembic upgrade | 5-10s |
| **TOTAL** | **3-4 minutos** |

---

## 🎯 Comandos Útiles Posteriores

### Ver logs de PostgreSQL
```powershell
docker logs -f amortizaciones_db
```

### Conectarse a la base de datos
```powershell
docker exec -it amortizaciones_db psql -U postgres -d amortizaciones_db
```

Luego en psql:
```sql
\dt                    -- Listar tablas
SELECT * FROM users;   -- Ver usuarios
\q                     -- Salir
```

### Detener servidor FastAPI
```powershell
Ctrl + C
```

### Desactivar entorno virtual
```powershell
deactivate
```

### Detener PostgreSQL
```powershell
docker-compose down
```

### Resetear todo (⚠️ borra datos)
```powershell
docker-compose down -v
docker-compose up -d
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

---

## 🚨 Errores Comunes y Soluciones

### Error: "connection timeout expired"
```powershell
# Solución: PostgreSQL tarda en estar listo
# Espera 30 segundos y reintenta
alembic upgrade head
```

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```powershell
# Solución: venv no está activado
# En Windows:
.\venv\Scripts\Activate.ps1
```

### Error: "Port 8000 already in use"
```powershell
# Solución: Usar otro puerto
uvicorn app.main:app --reload --port 8001
```

### Error: "FATAL: password authentication failed"
```powershell
# Solución: Resetear PostgreSQL
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

---

## 📱 Probar API desde PowerShell

```powershell
# Health check
Invoke-WebRequest http://localhost:8000/api/health

# Con más detalles
$response = Invoke-WebRequest http://localhost:8000/api/health
$response.Content | ConvertFrom-Json
```

---

## 🎉 ¡Listo!

Cuando veas esto en Terminal 2:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Tu backend está **100% funcional**. 

Accede a: **http://localhost:8000/api/docs**
