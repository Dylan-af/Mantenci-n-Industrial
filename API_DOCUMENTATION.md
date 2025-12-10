# API Mantención Industrial

## Descripción
API REST completa para gestionar sistemas de mantenimiento industrial con soporte para empresas, equipos, técnicos, planes de mantenimiento y órdenes de trabajo.

## Base URL
```
http://localhost:8000/api/
```

## Autenticación
La API soporta autenticación por sesión. Para login:
```
POST /api-auth/login/
```

## Endpoints Principales

### 1. EMPRESAS
**Base**: `/api/empresas/`

#### Listar empresas
```
GET /api/empresas/
```

#### Obtener detalles de empresa
```
GET /api/empresas/{id}/
```

#### Crear empresa
```
POST /api/empresas/
Body: {
  "nombre": "Empresa ABC",
  "rut": "12345678-9",
  "email": "contacto@empresa.cl",
  "telefono": "+56912345678",
  "direccion": "Calle Principal 123",
  "ciudad": "Santiago",
  "contacto_principal": "Juan Pérez"
}
```

#### Actualizar empresa
```
PUT /api/empresas/{id}/
PATCH /api/empresas/{id}/
```

#### Eliminar empresa
```
DELETE /api/empresas/{id}/
```

#### Empresas activas
```
GET /api/empresas/activas/
```

#### Estadísticas de empresa
```
GET /api/empresas/{id}/estadisticas/
```
Retorna: total_equipos, total_planes, total_ordenes, ordenes pendientes, costo total, horas trabajadas


### 2. EQUIPOS
**Base**: `/api/equipos/`

#### Listar equipos
```
GET /api/equipos/
```

#### Obtener detalles del equipo
```
GET /api/equipos/{id}/
```

#### Crear equipo
```
POST /api/equipos/
Body: {
  "empresa": 1,
  "nombre": "Bomba Hidráulica",
  "codigo": "EQ-001",
  "tipo": "Bomba",
  "marca": "Bosch",
  "modelo": "HV-2000",
  "serie": "SN123456",
  "ubicacion": "Planta A",
  "estado": "operativo",
  "fecha_adquisicion": "2023-01-15",
  "fecha_instalacion": "2023-02-01"
}
```

#### Equipos operativos
```
GET /api/equipos/operativos/
```

#### Equipos por empresa
```
GET /api/equipos/por-empresa/?empresa=1
```

#### Estadísticas del equipo
```
GET /api/equipos/{id}/estadisticas/
```


### 3. TÉCNICOS
**Base**: `/api/tecnicos/`

#### Listar técnicos
```
GET /api/tecnicos/
```

#### Crear técnico
```
POST /api/tecnicos/
Body: {
  "nombre": "Carlos",
  "apellido": "García",
  "rut": "19.123.456-7",
  "email": "carlos.garcia@empresa.cl",
  "telefono": "+56912345678",
  "especialidad": "mecanico",
  "experiencia_anos": 5,
  "certificaciones": "Certificado en Hidráulica"
}
```

#### Técnicos disponibles
```
GET /api/tecnicos/disponibles/
```

#### Técnicos por especialidad
```
GET /api/tecnicos/por-especialidad/?especialidad=mecanico
```
Especialidades: mecanico, electrico, hidraulico, electromecanico, general, otro

#### Técnicos por empresa
```
GET /api/tecnicos/por-empresa/?empresa=1
```


### 4. PLANES DE MANTENIMIENTO
**Base**: `/api/planes/`

#### Listar planes
```
GET /api/planes/
```

#### Crear plan
```
POST /api/planes/
Body: {
  "empresa": 1,
  "equipo": 1,
  "nombre": "Mantenimiento Preventivo Mensual",
  "tipo": "preventivo",
  "frecuencia": "mensual",
  "duracion_estimada_horas": 2.5,
  "tareas": "Revisar presión, limpiar filtros, cambiar aceite",
  "herramientas_requeridas": "Multímetro, llave inglesa",
  "repuestos_comunes": "Filtro, aceite",
  "costo_estimado": 50000,
  "fecha_inicio": "2025-01-01"
}
```

#### Planes activos
```
GET /api/planes/activos/
```

#### Planes próximos a vencer (7 días)
```
GET /api/planes/proximos_vencimientos/
```

#### Planes por equipo
```
GET /api/planes/por-equipo/?equipo=1
```


### 5. ÓRDENES DE TRABAJO
**Base**: `/api/ordenes/`

#### Listar órdenes
```
GET /api/ordenes/
```

#### Crear orden
```
POST /api/ordenes/
Body: {
  "empresa": 1,
  "equipo": 1,
  "plan": 1,
  "tecnico_asignado": 1,
  "descripcion": "Mantenimiento preventivo programado",
  "estado": "programada",
  "prioridad": "media",
  "fecha_programada": "2025-12-15T10:00:00Z"
}
```

#### Estados de orden: 
- programada
- en_progreso
- pausada
- completada
- cancelada
- pendiente

#### Prioridades:
- baja, media, alta, urgente

#### Iniciar orden
```
POST /api/ordenes/{id}/iniciar/
```

#### Completar orden
```
POST /api/ordenes/{id}/completar/
```

#### Pausar orden
```
POST /api/ordenes/{id}/pausar/
```

#### Cancelar orden
```
POST /api/ordenes/{id}/cancelar/
```

#### Órdenes pendientes
```
GET /api/ordenes/pendientes/
```

#### Órdenes urgentes
```
GET /api/ordenes/urgentes/
```

#### Órdenes vencidas
```
GET /api/ordenes/vencidas/
```

#### Órdenes por técnico
```
GET /api/ordenes/por-tecnico/?tecnico=1
```

#### Órdenes por técnico (alternativa)
```
GET /api/ordenes/por-tecnico/?tecnico=1
```


## Paginación

La mayoría de listados soportan paginación:
```
GET /api/empresas/?page=1&page_size=10
```

Parámetros:
- `page`: Número de página (defecto: 1)
- `page_size`: Elementos por página (máx: 100, defecto: 10)


## Búsqueda y Filtrado

### Búsqueda
```
GET /api/empresas/?search=nombre_empresa
GET /api/equipos/?search=código
GET /api/ordenes/?search=numero_orden
```

### Ordenamiento
```
GET /api/empresas/?ordering=-fecha_creacion
GET /api/tecnicos/?ordering=apellido
```

Use `-` para orden descendente.


## Ejemplos de Respuestas

### Empresa
```json
{
  "id": 1,
  "nombre": "Empresa ABC",
  "rut": "12345678-9",
  "email": "contacto@empresa.cl",
  "telefono": "+56912345678",
  "ciudad": "Santiago",
  "activa": true,
  "fecha_creacion": "2025-01-10T10:30:00Z",
  "fecha_actualizacion": "2025-12-10T15:45:00Z"
}
```

### Orden Completa
```json
{
  "id": 5,
  "numero_orden": "ORD-2025-00005",
  "empresa": 1,
  "empresa_nombre": "Empresa ABC",
  "equipo": 1,
  "equipo_nombre": "Bomba Hidráulica",
  "plan": 1,
  "plan_nombre": "Mantenimiento Preventivo",
  "tecnico_asignado": 1,
  "tecnico_nombre": "Carlos García",
  "descripcion": "Mantenimiento programado",
  "estado": "completada",
  "estado_display": "Completada",
  "prioridad": "media",
  "prioridad_display": "Media",
  "fecha_programada": "2025-12-15T10:00:00Z",
  "fecha_inicio": "2025-12-15T10:15:00Z",
  "fecha_termino": "2025-12-15T12:45:00Z",
  "horas_trabajadas": "2.50",
  "costo_real": "75000.00",
  "fecha_creacion": "2025-12-10T08:00:00Z"
}
```


## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Solicitud inválida
- `401 Unauthorized`: Autenticación requerida
- `403 Forbidden`: Acceso denegado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor


## Validaciones

### Orden
- Equipo debe pertenecer a la empresa especificada
- Fecha de inicio no puede ser posterior a fecha de término
- Horas trabajadas deben ser positivas

### Plan
- El equipo debe pertenecer a la empresa

### Equipo
- Código debe ser único
- Combinación empresa+código debe ser única


## Filtros Disponibles

### Empresas
- search: nombre, rut, email, ciudad
- ordering: nombre, fecha_creacion

### Equipos
- search: nombre, codigo, tipo, marca
- ordering: nombre, estado, fecha_ultimo_mantenimiento

### Técnicos
- search: nombre, apellido, rut, email, especialidad
- ordering: apellido, experiencia_anos, fecha_contratacion

### Planes
- search: nombre, tipo, frecuencia
- ordering: nombre, tipo, fecha_inicio

### Órdenes
- search: numero_orden, equipo.nombre, descripcion
- ordering: fecha_programada, prioridad, estado


## Autenticación y Autorización

Actualmente se usa autenticación por sesión. Para endpoints protegidos:

```bash
curl -X GET http://localhost:8000/api/empresas/ \
  -b "sessionid=..." \
  -H "Content-Type: application/json"
```

Puede usar login:
```bash
curl -X POST http://localhost:8000/api-auth/login/ \
  -d "username=admin&password=admin" \
  -c cookies.txt

curl -X GET http://localhost:8000/api/empresas/ \
  -b cookies.txt
```


## Desarrollo

### Ejecutar servidor
```bash
python manage.py runserver
```

### Ver logs
```bash
python manage.py runserver --verbosity 2
```

### Crear datos de prueba
```bash
python manage.py shell
```

Luego en shell:
```python
from mantenimiento.models import Empresa
Empresa.objects.create(
    nombre="Empresa Test",
    rut="11111111-1",
    email="test@test.cl"
)
```
