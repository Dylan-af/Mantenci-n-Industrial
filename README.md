# Mantención Industrial - Backend Django

## Configuración Inicial

### Requisitos
- Python 3.8+
- pip

### Instalación

1. **Crear y activar ambiente virtual** (si no existe):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

### Paquetes Instalados
- **Django 6.0**: Framework web de alto nivel
- **Django REST Framework 3.16.1**: Herramienta para construir APIs REST

### Estructura del Proyecto

```
.
├── config/              # Configuración principal del proyecto
│   ├── settings.py      # Configuraciones de Django y DRF
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuración WSGI
├── mantenimiento/       # Aplicación de mantenimiento
│   ├── models.py        # Modelos de datos
│   ├── views.py         # Vistas y ViewSets
│   ├── serializers.py   # Serializadores de DRF
│   └── urls.py          # URLs de la aplicación
├── manage.py            # Script de gestión de Django
├── db.sqlite3           # Base de datos SQLite
└── requirements.txt     # Dependencias del proyecto
```

### Comandos Útiles

```bash
# Activar ambiente virtual
.\venv\Scripts\activate  # Windows

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear nueva aplicación
python manage.py startapp nombre_app

# Crear migraciones para modelos
python manage.py makemigrations

# Ver migraciones pendientes
python manage.py showmigrations
```

### Credenciales Admin
- **Usuario**: admin
- **Email**: admin@example.com
- **Contraseña**: (configurable)

### Acceder a Django Admin
Una vez ejecutando el servidor:
```
http://127.0.0.1:8000/admin
```

### Configuración de Django REST Framework

El proyecto incluye configuración básica de DRF:
- Paginación: 10 elementos por página
- Filtros de búsqueda y ordenamiento habilitados
- Serialización JSON

### Próximos Pasos

1. Definir modelos en `mantenimiento/models.py`
2. Crear serializadores en `mantenimiento/serializers.py`
3. Implementar ViewSets en `mantenimiento/views.py`
4. Configurar URLs en `mantenimiento/urls.py` y `config/urls.py`
5. Ejecutar `python manage.py makemigrations` y `python manage.py migrate`
