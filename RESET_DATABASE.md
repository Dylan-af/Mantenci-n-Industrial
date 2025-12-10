# Comandos para resetear BD y migraciones

# 1. Activar ambiente virtual
.\venv\Scripts\Activate.ps1

# 2. Eliminar la BD actual
Remove-Item db.sqlite3 -Force

# 3. Eliminar las migraciones antiguas (excepto __init__.py)
Get-ChildItem mantenimiento\migrations\*.py | Where-Object {$_.Name -ne "__init__.py"} | Remove-Item -Force

# 4. Crear nuevas migraciones
python manage.py makemigrations

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear nuevo superusuario
python manage.py createsuperuser

# 7. Verificar que todo está bien
python manage.py check

# 8. Ejecutar servidor
python manage.py runserver
