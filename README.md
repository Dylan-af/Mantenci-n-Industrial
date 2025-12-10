# Mantención Industrial - Sistema de Gestión de Mantenimiento

Sistema completo de API REST para gestionar mantenimiento industrial con soporte para empresas, equipos, técnicos, planes de mantenimiento y órdenes de trabajo.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Documentation](#api-documentation)
- [Autenticación y Permisos](#autenticación-y-permisos)
- [Desarrollo](#desarrollo)

## ✨ Características

- ✅ **Gestión de Empresas**: Registro y administración de clientes
- ✅ **Gestión de Equipos**: Control de activos con historial de mantenimiento
- ✅ **Gestión de Técnicos**: Personal técnico con especialidades
- ✅ **Planes de Mantenimiento**: Preventivo, correctivo y predictivo
- ✅ **Órdenes de Trabajo**: Creación, seguimiento y control de trabajos
- ✅ **API REST Completa**: Endpoints documentados para integración
- ✅ **Autenticación**: Sistema de permisos IsAuthenticatedOrReadOnly
- ✅ **Paginación y Filtrado**: Búsqueda avanzada en todos los recursos
- ✅ **Estadísticas**: Reportes de empresas y equipos
- ✅ **Admin Django**: Panel administrativo completo

## 📦 Requisitos

- **Python**: 3.8+
- **pip**: Gestor de paquetes de Python
- **Git**: Control de versiones (opcional)

### Paquetes Principales

- Django 6.0
- Django REST Framework 3.16.1
- coreapi 2.3.3

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Dylan-af/Mantenci-n-Industrial.git
cd Mantenci-n-Industrial
```

### 2. Crear Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install Django==6.0
pip install djangorestframework==3.16.1
pip install coreapi==2.3.3
```

### 4. Aplicar Migraciones

```bash
python manage.py migrate
```

Salida esperada:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, mantenimiento, sessions
Running migrations:
  Applying mantenimiento.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### 5. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingrese:
- Username: `admin`
- Email: `admin@example.com`
- Password: (elija una contraseña segura)

### 6. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

La API estará disponible en: `http://127.0.0.1:8000/`

## ⚙️ Configuración

### Cambiar Zona Horaria

En `config/settings.py`:
```python
TIME_ZONE = 'America/Santiago'  # Para Chile
# o
TIME_ZONE = 'UTC'  # Para UTC
```

### Cambiar Idioma

En `config/settings.py`:
```python
LANGUAGE_CODE = 'es-es'  # Español
# o
LANGUAGE_CODE = 'en-us'  # Inglés
```

### Configuración de Base de Datos

**SQLite (Defecto - Desarrollo):**
Ya está configurada en `config/settings.py`

**PostgreSQL (Producción):**
```bash
pip install psycopg2-binary
```

En `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mantenccion_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configuración de CORS (Opcional)

Para permitir peticiones desde diferentes dominios:

```bash
pip install django-cors-headers
```

En `config/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## 📖 Uso

### Acceder al Panel Admin

1. Ejecutar servidor: `python manage.py runserver`
2. Ir a: `http://127.0.0.1:8000/admin/`
3. Loguear con superusuario
4. Crear empresas, equipos, técnicos, planes y órdenes

### Usar la API

**Listar todas las empresas:**
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/
```

**Crear una nueva empresa (requiere autenticación):**
```bash
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Empresa ABC",
    "rut": "12345678-9",
    "email": "contacto@empresa.cl"
  }' \
  -u admin:password
```

**Ver detalles de una empresa:**
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/1/
```

**Obtener estadísticas de una empresa:**
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/1/estadisticas/
```

**Filtrar equipos operativos:**
```bash
curl -X GET http://127.0.0.1:8000/api/equipos/operativos/
```

**Listar órdenes pendientes:**
```bash
curl -X GET http://127.0.0.1:8000/api/ordenes/pendientes/
```

**Iniciar una orden:**
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/5/iniciar/ \
  -u admin:password
```

## 📁 Estructura del Proyecto

```
Mantenci-n-Industrial/
├── config/                      # Configuración principal
│   ├── settings.py             # Configuraciones de Django
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # Servidor WSGI
│   └── asgi.py                 # Servidor ASGI
├── mantenimiento/              # Aplicación principal
│   ├── models.py               # Modelos de datos
│   ├── views.py                # ViewSets y vistas
│   ├── serializers.py          # Serializadores de datos
│   ├── urls.py                 # URLs de la app
│   ├── admin.py                # Configuración del admin
│   └── migrations/             # Migraciones de BD
├── manage.py                   # Script de gestión
├── db.sqlite3                  # Base de datos
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── API_DOCUMENTATION.md        # Documentación API
└── venv/                       # Ambiente virtual
```

## 🔌 API Documentation

Ver [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) para:
- Endpoints completos
- Ejemplos de requests
- Códigos de respuesta
- Filtros y búsqueda
- Validaciones

### Endpoints Rápidos

**Empresas:**
- `GET /api/empresas/` - Listar
- `POST /api/empresas/` - Crear
- `GET /api/empresas/{id}/` - Detalles
- `GET /api/empresas/{id}/estadisticas/` - Estadísticas
- `GET /api/empresas/activas/` - Solo activas

**Equipos:**
- `GET /api/equipos/` - Listar
- `GET /api/equipos/operativos/` - Solo operativos
- `GET /api/equipos/{id}/estadisticas/` - Estadísticas

**Técnicos:**
- `GET /api/tecnicos/` - Listar
- `GET /api/tecnicos/disponibles/` - Solo activos
- `GET /api/tecnicos/por-especialidad/?especialidad=mecanico`

**Planes:**
- `GET /api/planes/` - Listar
- `GET /api/planes/activos/` - Solo activos
- `GET /api/planes/proximos_vencimientos/` - Próximas 7 días

**Órdenes:**
- `GET /api/ordenes/` - Listar
- `POST /api/ordenes/{id}/iniciar/` - Iniciar orden
- `POST /api/ordenes/{id}/completar/` - Completar orden
- `GET /api/ordenes/pendientes/` - Órdenes pendientes
- `GET /api/ordenes/urgentes/` - Órdenes urgentes

## 🔐 Autenticación y Permisos

### Sistema de Permisos

**IsAuthenticatedOrReadOnly:**
- ✅ Usuarios anónimos: Pueden **leer** (GET)
- ✅ Usuarios autenticados: Pueden **crear, editar, eliminar**

### Login

**Por sesión (Panel Admin):**
```bash
curl -X POST http://127.0.0.1:8000/api-auth/login/ \
  -d "username=admin&password=password"
```

**Con curl y autenticación básica:**
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/ \
  -u admin:password
```

**Obtener token de sesión:**
```bash
curl -X POST http://127.0.0.1:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

## 🛠️ Desarrollo

### Comandos Útiles

**Ejecutar servidor con más detalles:**
```bash
python manage.py runserver --verbosity 2
```

**Acceder a shell de Django:**
```bash
python manage.py shell
```

En el shell:
```python
from mantenimiento.models import Empresa, Equipo
empresa = Empresa.objects.create(
    nombre="Mi Empresa",
    rut="12345678-9",
    email="contacto@empresa.cl"
)
print(f"Empresa creada: {empresa}")
```

**Crear migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Ver migraciones pendientes:**
```bash
python manage.py showmigrations
```

**Revertir migraciones:**
```bash
python manage.py migrate mantenimiento 0001
```

**Crear app nueva:**
```bash
python manage.py startapp nombre_app
```

**Recolectar archivos estáticos:**
```bash
python manage.py collectstatic
```

### Ejecutar Pruebas

```bash
python manage.py test
```

### Generar Datos de Prueba

Crear archivo `populate_db.py`:
```python
from mantenimiento.models import Empresa, Equipo, Tecnico

# Crear empresa
empresa = Empresa.objects.create(
    nombre="Empresa Test",
    rut="99.999.999-9",
    email="test@empresa.cl",
    ciudad="Santiago"
)

# Crear equipo
equipo = Equipo.objects.create(
    empresa=empresa,
    nombre="Bomba Centrífuga",
    codigo="EQ-001",
    tipo="Bomba",
    marca="Grundfos",
    modelo="NK 100-250",
    estado="operativo"
)

# Crear técnico
tecnico = Tecnico.objects.create(
    nombre="Juan",
    apellido="Pérez",
    rut="18.123.456-7",
    email="juan@tecnico.cl",
    telefono="+56912345678",
    especialidad="mecanico",
    experiencia_anos=5
)

print("✅ Datos de prueba creados exitosamente")
```

Ejecutar:
```bash
python manage.py shell < populate_db.py
```

## 📊 Modelos de Datos

### Empresa
- nombre, rut, email, teléfono
- dirección, ciudad, contacto
- estado (activa/inactiva)

### Equipo
- nombre, código, tipo
- marca, modelo, serie
- ubicación, estado
- fechas de adquisición, instalación, último mantenimiento

### Técnico
- nombre, apellido, rut, email
- especialidad (mecánico, eléctrico, etc.)
- años de experiencia
- certificaciones

### Plan
- nombre, descripción
- tipo (preventivo, correctivo, predictivo)
- frecuencia (diaria, semanal, mensual, etc.)
- duración estimada, costo
- tareas, herramientas, repuestos

### Orden
- número automático (ORD-AÑO-XXXXX)
- equipo, empresa, plan
- técnico asignado
- estado, prioridad
- fechas programada, inicio, término
- horas trabajadas, costo real

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución:**
```bash
# Asegurar que el venv está activado
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "CommandError: System check identified some issues"

```bash
python manage.py check
```

Esto mostrará los problemas específicos.

### Error: "Could not open database"

Eliminar `db.sqlite3` y recrear:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Puerto 8000 ya en uso

```bash
python manage.py runserver 8001
```

## 📝 Notas

- La base de datos SQLite es solo para desarrollo
- Para producción usar PostgreSQL o MySQL
- Cambiar `DEBUG = False` en producción
- Generar `SECRET_KEY` segura en producción
- Configurar `ALLOWED_HOSTS` en producción
