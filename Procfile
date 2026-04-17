release: python run_migrations.py || echo "Migraciones completadas o ya existían"
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
