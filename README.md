# 🔧 Mantención Industrial - Sistema de Gestión

Sistema completo de API REST para demostrar gestión integral de mantenimiento industrial. Incluye empresas, equipos, técnicos, planes de mantenimiento y órdenes de trabajo.

## ⚡ Inicio Rápido 

### 1. Activar Ambiente Virtual
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 2. Correr el Servidor
```bash
python manage.py runserver
```

### 3. Acceder a la Aplicación
- **API REST**: http://127.0.0.1:8000/api/
- **Panel Admin**: http://127.0.0.1:8000/admin/
  - Usuario: `admin`
  - Contraseña: `admin`

## 📦 Requisitos

- **Python**: 3.8+
- **pip**: Gestor de paquetes de Python
- **Git**: Control de versiones (opcional)

### Paquetes Principales

- Django 6.0
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
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

### 4. Aplicar Migraciones

```bash
python manage.py migrate
```

### 5. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

La API estará disponible en: `http://127.0.0.1:8000/`

### 🏢 Módulo de Empresas
Gestiona clientes/empresas con toda su información:
- Nombre, RUT, email, teléfono
- Dirección, ciudad, contacto principal
- Equipos, planes y órdenes asociadas
- Estadísticas en tiempo real

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "nombre": "Minería ABC",
  "rut": "78.123.456-7",
  "email": "contacto@mineria.cl",
  "ciudad": "Antofagasta",
  "total_equipos": 5,
  "total_ordenes": 23
}
```

### ⚙️ Módulo de Equipos
Control de activos industriales:
- Especificaciones técnicas (marca, modelo, serie)
- Estado operativo (operativo, mantenimiento, etc.)
- Historial de mantenimiento
- Campo crítico para equipos de importancia alta
- Ubicación y datos de adquisición

**Ejemplo:**
```json
{
  "id": 1,
  "nombre": "Compresor Industrial",
  "codigo": "EQ-001",
  "tipo": "Compresor",
  "marca": "Atlas Copco",
  "estado": "operativo",
  "critical": true,
  "fecha_ultimo_mantenimiento": "2025-11-20"
}
```

### 👨‍🔧 Módulo de Técnicos
Personal técnico especializado:
- Datos personales y profesionales
- Especialidades (mecánico, eléctrico, etc.)
- Años de experiencia
- Usuario del sistema para login directo
- Asignación a empresas específicas

**Ejemplo:**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "García",
  "especialidad": "mecanico",
  "experiencia_anos": 8,
  "user": 2
}
```

### 📋 Módulo de Planes
Planes de mantenimiento configurables:
- Tipos: Preventivo, Correctivo, Predictivo
- Frecuencias: Diaria, Semanal, Mensual, Trimestral, etc.
- **Nuevo**: Frecuencia en días para cálculos automáticos
- Tareas, herramientas y repuestos
- Costos estimados
- Técnicos recomendados

**Ejemplo:**
```json
{
  "id": 1,
  "nombre": "Mantenimiento Mensual",
  "tipo": "preventivo",
  "frecuencia": "mensual",
  "frequency_days": 30,
  "duracion_estimada_horas": 2.5,
  "costo_estimado": 150000
}
```

### 📍 Módulo de Órdenes
Órdenes de trabajo con seguimiento completo:
- Numeración automática (ORD-2025-00001)
- Estados: Programada, En Progreso, Completada, etc.
- Prioridades: Baja, Media, Alta, Urgente
- Asignación de técnicos
- Seguimiento de tiempo y costos reales

**Estados de una orden:**
```
Programada → En Progreso → Completada
                    ↓
                 Pausada → En Progreso → Completada
                    ↓
                Cancelada (fin)
```

### Crear una Empresa
```bash
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "TechMining Ltd",
    "rut": "99.999.999-9",
    "email": "info@techmining.cl",
    "ciudad": "Santiago"
  }' \
  -u admin:admin
```

### Crear un Equipo
```bash
curl -X POST http://127.0.0.1:8000/api/equipos/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "nombre": "Bomba Centrífuga HP-500",
    "codigo": "EQ-001",
    "tipo": "Bomba",
    "marca": "Grundfos",
    "critical": true,
    "estado": "operativo"
  }' \
  -u admin:admin
```

### Crear un Técnico con Usuario
```bash
curl -X POST http://127.0.0.1:8000/api/tecnicos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "rut": "18.456.789-2",
    "email": "carlos@tecnico.cl",
    "telefono": "+56912345678",
    "especialidad": "mecanico",
    "experiencia_anos": 10
  }' \
  -u admin:admin
```

### Crear un Plan de Mantenimiento
```bash
curl -X POST http://127.0.0.1:8000/api/planes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "equipo": 1,
    "nombre": "Mantenimiento Trimestral - Bomba",
    "tipo": "preventivo",
    "frecuencia": "trimestral",
    "frequency_days": 90,
    "duracion_estimada_horas": 3.5,
    "tareas": "Inspección completa, cambio de aceite, revisión de sellos",
    "fecha_inicio": "2025-12-01"
  }' \
  -u admin:admin
```

### Crear una Orden de Trabajo
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "equipo": 1,
    "plan": 1,
    "tecnico_asignado": 1,
    "descripcion": "Mantenimiento preventivo programado",
    "estado": "programada",
    "prioridad": "media",
    "fecha_programada": "2025-12-15T10:00:00Z"
  }' \
  -u admin:admin
```

### Iniciar una Orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/1/iniciar/ -u admin:admin
```

### Completar una Orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/1/completar/ \
  -H "Content-Type: application/json" \
  -d '{
    "horas_trabajadas": 3.25,
    "costo_real": 145000,
    "observaciones": "Todo en orden"
  }' \
  -u admin:admin
```

## 📊 Endpoints Principales

| Recurso | GET | POST | PUT | DELETE |
|---------|-----|------|-----|--------|
| `/api/empresas/` | ✅ | ✅ | ✅ | ✅ |
| `/api/equipos/` | ✅ | ✅ | ✅ | ✅ |
| `/api/tecnicos/` | ✅ | ✅ | ✅ | ✅ |
| `/api/planes/` | ✅ | ✅ | ✅ | ✅ |
| `/api/ordenes/` | ✅ | ✅ | ✅ | ✅ |

### Acciones Especiales

**Empresas:**
- `GET /api/empresas/activas/` - Solo empresas activas
- `GET /api/empresas/{id}/estadisticas/` - Métricas de empresa

**Equipos:**
- `GET /api/equipos/operativos/` - Solo operativos
- `GET /api/equipos/{id}/estadisticas/` - Métricas de equipo

**Técnicos:**
- `GET /api/tecnicos/disponibles/` - Técnicos activos
- `GET /api/tecnicos/por-especialidad/?especialidad=mecanico`

**Planes:**
- `GET /api/planes/activos/` - Planes vigentes
- `GET /api/planes/proximos_vencimientos/` - Próximos 7 días

**Órdenes:**
- `GET /api/ordenes/pendientes/` - Órdenes sin completar
- `POST /api/ordenes/{id}/iniciar/` - Iniciar trabajo
- `POST /api/ordenes/{id}/completar/` - Finalizar trabajo
- `POST /api/ordenes/{id}/pausar/` - Pausar trabajo
- `POST /api/ordenes/{id}/cancelar/` - Cancelar trabajo

## 🔐 Autenticación JWT

La API utiliza **JWT (JSON Web Tokens)** para autenticación segura. Ventajas:
- ✅ Tokens expirables
- ✅ Refresh tokens para renovación
- ✅ Sin almacenar sesiones en servidor
- ✅ Escalable para microservicios

### Obtener Token JWT

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

**Respuesta:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usar el Token de Acceso

```bash
curl -X GET http://127.0.0.1:8000/api/empresas/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Renovar Token Expirado

El `access` token expira en 1 hora. Usa el `refresh` token para renovar:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Configuración JWT

En `config/settings.py`:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## 🛠️ Tecnologías Usadas

- **Django 6.0** - Framework web Python
- **Django REST Framework 3.16.1** - API REST
- **SQLite** - Base de datos (demostración)
- **Python 3.8+** - Lenguaje

## 📁 Estructura del Proyecto

```
Mantenci-n-Industrial/
├── config/
│   ├── settings.py          ← Configuraciones
│   ├── urls.py              ← Rutas principales
│   └── wsgi.py
├── mantenimiento/
│   ├── models.py            ← 5 modelos
│   ├── views.py             ← 5 ViewSets
│   ├── serializers.py       ← Serializadores
│   ├── admin.py             ← Panel admin
│   └── urls.py
├── db.sqlite3               ← Base de datos
├── manage.py                ← Gestor Django
└── requirements.txt         ← Dependencias
```

## 💾 Datos de Prueba

### Acceso por Defecto
- **Usuario:** admin
- **Contraseña:** admin

### Crear Datos de Demo
```bash
python manage.py shell
```

Luego en el shell:
```python
from mantenimiento.models import Empresa, Equipo, Tecnico

# Crear empresa
empresa = Empresa.objects.create(
    nombre="Demo Corp",
    rut="11.111.111-1",
    email="demo@corp.cl",
    ciudad="Santiago"
)

# Crear equipo
equipo = Equipo.objects.create(
    empresa=empresa,
    nombre="Motor Eléctrico",
    codigo="DEMO-001",
    tipo="Motor",
    critical=False
)

# Crear técnico
tecnico = Tecnico.objects.create(
    nombre="Pedro",
    apellido="Pérez",
    rut="17.000.000-0",
    email="pedro@demo.cl",
    telefono="+56900000000",
    especialidad="electrico",
    experiencia_anos=5
)

print("✅ Datos de demo creados")
```

## 📖 Documentación Adicional

- `QUICKSTART.md` - Inicio rápido
- `API_DOCUMENTATION.md` - Referencia completa de API
- `API_EXAMPLES.md` - +50 ejemplos prácticos
- `PROJECT_SUMMARY.md` - Resumen del proyecto

## 🎬 Casos de Uso

### Caso 1: Crear y Completar una Orden
1. Crear empresa
2. Crear equipo en esa empresa
3. Crear técnico
4. Crear plan de mantenimiento
5. Crear orden
6. Cambiar estado: Programada → En Progreso → Completada

### Caso 2: Ver Estadísticas
1. Acceder a `/api/empresas/1/estadisticas/`
2. Ver métricas: equipos, órdenes, costos, horas
3. Acceder a `/api/equipos/1/estadisticas/`
4. Analizar historial de mantenimiento

### Caso 3: Filtrar y Buscar
1. Buscar equipos: `?search=codigo`
2. Filtrar críticos: Crear equipos con `critical=true`
3. Ordenar por fecha: `?ordering=-fecha_creacion`