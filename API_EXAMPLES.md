# Ejemplos de Uso - API Mantención Industrial

## 📝 Ejemplos con cURL

### Autenticación

**Login (obtener sesión):**
```bash
curl -X POST http://127.0.0.1:8000/api-auth/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin" \
  -c cookies.txt
```

**Usar sesión guardada:**
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/ \
  -b cookies.txt
```

---

## 🏢 Empresas

### Listar todas las empresas (lectura pública)
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/
```

### Crear empresa (requiere autenticación)
```bash
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Minería ABC",
    "rut": "78.123.456-7",
    "email": "contacto@mineria.cl",
    "telefono": "+56912345678",
    "direccion": "Avenida Principal 456",
    "ciudad": "Antofagasta",
    "contacto_principal": "María González",
    "descripcion": "Empresa de minería y extracción"
  }' \
  -u admin:password
```

### Obtener detalles de una empresa
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/1/
```

### Actualizar empresa
```bash
curl -X PATCH http://127.0.0.1:8000/api/empresas/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "+56987654321",
    "ciudad": "Valparaíso"
  }' \
  -u admin:password
```

### Listar solo empresas activas
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/activas/
```

### Estadísticas de empresa
```bash
curl -X GET http://127.0.0.1:8000/api/empresas/1/estadisticas/
```

Respuesta:
```json
{
  "total_equipos": 5,
  "total_planes": 8,
  "total_ordenes": 23,
  "ordenes_pendientes": 3,
  "ordenes_en_progreso": 1,
  "ordenes_completadas": 19,
  "costo_total_ordenes": "1250000.00",
  "horas_totales_trabajadas": "145.50"
}
```

---

## ⚙️ Equipos

### Listar todos los equipos
```bash
curl -X GET http://127.0.0.1:8000/api/equipos/
```

### Crear equipo
```bash
curl -X POST http://127.0.0.1:8000/api/equipos/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "nombre": "Compresor Industrial CP-500",
    "codigo": "EQ-0012",
    "tipo": "Compresor",
    "marca": "Atlas Copco",
    "modelo": "GA 50VSD FF",
    "serie": "SN-AC-2023-0001",
    "ubicacion": "Planta Principal - Taller B",
    "estado": "operativo",
    "fecha_adquisicion": "2022-06-15",
    "fecha_instalacion": "2022-07-01",
    "fecha_ultimo_mantenimiento": "2025-11-20",
    "descripcion": "Compresor de aire rotativo de tornillo"
  }' \
  -u admin:password
```

### Filtrar equipos por estado
```bash
curl -X GET "http://127.0.0.1:8000/api/equipos/?search=EQ-001"
```

### Equipos operativos
```bash
curl -X GET http://127.0.0.1:8000/api/equipos/operativos/
```

### Equipos de una empresa
```bash
curl -X GET "http://127.0.0.1:8000/api/equipos/por-empresa/?empresa=1"
```

### Estadísticas de equipo
```bash
curl -X GET http://127.0.0.1:8000/api/equipos/1/estadisticas/
```

Respuesta:
```json
{
  "nombre_equipo": "Compresor Industrial CP-500",
  "total_ordenes": 8,
  "ordenes_completadas": 7,
  "dias_sin_mantenimiento": 20,
  "proxima_mantencion": "2026-01-20",
  "costo_total_mantenimiento": "450000.00",
  "horas_totales_trabajadas": "36.75"
}
```

---

## 👨‍🔧 Técnicos

### Listar técnicos
```bash
curl -X GET http://127.0.0.1:8000/api/tecnicos/
```

### Crear técnico
```bash
curl -X POST http://127.0.0.1:8000/api/tecnicos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Roberto",
    "apellido": "Valenzuela",
    "rut": "16.789.456-3",
    "email": "r.valenzuela@tecnico.cl",
    "telefono": "+56998765432",
    "especialidad": "electromecanico",
    "experiencia_anos": 8,
    "certificaciones": "Certificado IEC 61936, Especialista en sistemas hidráulicos"
  }' \
  -u admin:password
```

### Técnicos disponibles (activos)
```bash
curl -X GET http://127.0.0.1:8000/api/tecnicos/disponibles/
```

### Técnicos por especialidad
```bash
curl -X GET "http://127.0.0.1:8000/api/tecnicos/por-especialidad/?especialidad=mecanico"
```

Especialidades disponibles:
- mecanico
- electrico
- hidraulico
- electromecanico
- general
- otro

### Técnicos por empresa
```bash
curl -X GET "http://127.0.0.1:8000/api/tecnicos/por-empresa/?empresa=1"
```

### Asignar técnico a empresa
```bash
curl -X PATCH http://127.0.0.1:8000/api/tecnicos/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresas": [1, 2]
  }' \
  -u admin:password
```

---

## 📋 Planes de Mantenimiento

### Listar planes
```bash
curl -X GET http://127.0.0.1:8000/api/planes/
```

### Crear plan preventivo
```bash
curl -X POST http://127.0.0.1:8000/api/planes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "equipo": 1,
    "nombre": "Mantenimiento Preventivo Trimestral - Compresor",
    "descripcion": "Revisión completa y servicio del compresor",
    "tipo": "preventivo",
    "frecuencia": "trimestral",
    "duracion_estimada_horas": 4.5,
    "tareas": "1. Inspeccionar filtros de aire\n2. Revisar presión de descarga\n3. Cambiar aceite del compresor\n4. Limpiar radiador\n5. Verificar correas",
    "herramientas_requeridas": "Manómetro, llave inglesa, destornillador",
    "repuestos_comunes": "Filtro de aire, aceite compressor 32ISO, correas",
    "costo_estimado": 150000,
    "fecha_inicio": "2025-12-15"
  }' \
  -u admin:password
```

### Planes activos
```bash
curl -X GET http://127.0.0.1:8000/api/planes/activos/
```

### Planes próximos a vencer (7 días)
```bash
curl -X GET http://127.0.0.1:8000/api/planes/proximos_vencimientos/
```

### Planes de un equipo
```bash
curl -X GET "http://127.0.0.1:8000/api/planes/por-equipo/?equipo=1"
```

### Actualizar plan
```bash
curl -X PATCH http://127.0.0.1:8000/api/planes/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_proximo_mantenimiento": "2026-03-15",
    "costo_estimado": 175000
  }' \
  -u admin:password
```

---

## 📍 Órdenes de Trabajo

### Listar órdenes
```bash
curl -X GET http://127.0.0.1:8000/api/ordenes/
```

### Crear orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "equipo": 1,
    "plan": 1,
    "tecnico_asignado": 1,
    "descripcion": "Mantenimiento preventivo trimestral del compresor según plan",
    "estado": "programada",
    "prioridad": "media",
    "fecha_programada": "2025-12-18T09:00:00Z"
  }' \
  -u admin:password
```

### Órdenes pendientes
```bash
curl -X GET http://127.0.0.1:8000/api/ordenes/pendientes/
```

### Órdenes urgentes pendientes
```bash
curl -X GET http://127.0.0.1:8000/api/ordenes/urgentes/
```

### Órdenes vencidas
```bash
curl -X GET http://127.0.0.1:8000/api/ordenes/vencidas/
```

### Órdenes de un técnico
```bash
curl -X GET "http://127.0.0.1:8000/api/ordenes/por-tecnico/?tecnico=1"
```

### Iniciar orden (cambiar estado a en progreso)
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/5/iniciar/ \
  -H "Content-Type: application/json" \
  -u admin:password
```

Respuesta:
```json
{
  "id": 5,
  "numero_orden": "ORD-2025-00005",
  "estado": "en_progreso",
  "fecha_inicio": "2025-12-18T10:15:30.123456Z",
  ...
}
```

### Completar orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/5/completar/ \
  -H "Content-Type: application/json" \
  -d '{
    "observaciones": "Mantenimiento completado sin problemas",
    "repuestos_utilizados": "Filtro de aire, 2L aceite compressor",
    "horas_trabajadas": 4.25,
    "costo_real": 145000
  }' \
  -u admin:password
```

### Pausar orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/5/pausar/ \
  -H "Content-Type: application/json" \
  -u admin:password
```

### Cancelar orden
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/5/cancelar/ \
  -H "Content-Type: application/json" \
  -d '{
    "observaciones": "Cancelada por solicitud del cliente"
  }' \
  -u admin:password
```

---

## 🔍 Búsqueda y Filtrado

### Buscar empresas por nombre
```bash
curl -X GET "http://127.0.0.1:8000/api/empresas/?search=Minería"
```

### Buscar equipos por código
```bash
curl -X GET "http://127.0.0.1:8000/api/equipos/?search=EQ-001"
```

### Ordenar por nombre descendente
```bash
curl -X GET "http://127.0.0.1:8000/api/empresas/?ordering=-nombre"
```

### Paginación
```bash
curl -X GET "http://127.0.0.1:8000/api/ordenes/?page=2&page_size=5"
```

---

## 📊 Ejemplos Avanzados

### Flujo completo de creación de orden

1. **Crear empresa:**
```bash
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"MiEmpresa","rut":"12.345.678-9","email":"info@miempresa.cl"}' \
  -u admin:password
```

2. **Crear equipo:**
```bash
curl -X POST http://127.0.0.1:8000/api/equipos/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "nombre": "Bomba",
    "codigo": "BOMBA-001",
    "tipo": "Bomba"
  }' \
  -u admin:password
```

3. **Crear técnico:**
```bash
curl -X POST http://127.0.0.1:8000/api/tecnicos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Juan","apellido":"Pérez","rut":"18.123.456-7",
    "email":"juan@tecnico.cl","telefono":"+56912345678",
    "especialidad":"mecanico","experiencia_anos":5
  }' \
  -u admin:password
```

4. **Crear plan:**
```bash
curl -X POST http://127.0.0.1:8000/api/planes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa":1,"equipo":1,"nombre":"Plan Mensual",
    "tipo":"preventivo","frecuencia":"mensual",
    "duracion_estimada_horas":2,"tareas":"Inspeccionar",
    "fecha_inicio":"2025-12-01"
  }' \
  -u admin:password
```

5. **Crear orden:**
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/ \
  -H "Content-Type: application/json" \
  -d '{
    "empresa":1,"equipo":1,"plan":1,"tecnico_asignado":1,
    "descripcion":"Mantenimiento","estado":"programada",
    "prioridad":"media","fecha_programada":"2025-12-20T10:00:00Z"
  }' \
  -u admin:password
```

6. **Iniciar orden:**
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/1/iniciar/ \
  -u admin:password
```

7. **Completar orden:**
```bash
curl -X POST http://127.0.0.1:8000/api/ordenes/1/completar/ \
  -H "Content-Type: application/json" \
  -d '{"horas_trabajadas":2.5,"costo_real":50000}' \
  -u admin:password
```

---

## 🐍 Ejemplos con Python

### Instalación de requests
```bash
pip install requests
```

### Script de ejemplo
```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
AUTH = ("admin", "password")

# Crear empresa
response = requests.post(
    f"{BASE_URL}/empresas/",
    json={
        "nombre": "Empresa Python",
        "rut": "99.999.999-9",
        "email": "python@empresa.cl"
    },
    auth=AUTH
)
print(f"Empresa creada: {response.status_code}")
empresa_id = response.json()['id']

# Crear equipo
response = requests.post(
    f"{BASE_URL}/equipos/",
    json={
        "empresa": empresa_id,
        "nombre": "Motor Eléctrico",
        "codigo": "MOT-001",
        "tipo": "Motor"
    },
    auth=AUTH
)
equipo_id = response.json()['id']

# Listar órdenes
response = requests.get(f"{BASE_URL}/ordenes/")
ordenes = response.json()
print(f"Total órdenes: {ordenes['count']}")

# Filtrar órdenes pendientes
response = requests.get(f"{BASE_URL}/ordenes/pendientes/")
pendientes = response.json()
for orden in pendientes['results']:
    print(f"- {orden['numero_orden']}: {orden['estado']}")
```

---

## 📌 Notas Importantes

- **Autenticación requerida:** Para POST, PUT, PATCH, DELETE se requiere autenticación
- **Lectura pública:** Todos pueden hacer GET sin autenticación
- **Formato de fecha:** ISO 8601 (2025-12-18T10:00:00Z)
- **Números decimales:** Use strings para valores monetarios en algunos clientes
- **Validaciones:** El servidor valida datos y retorna errores 400

## ⚠️ Códigos de Error Comunes

```json
{
  "400": "Datos inválidos - revisar formato",
  "401": "No autenticado - hacer login",
  "403": "Sin permisos - solo usuarios autenticados",
  "404": "Recurso no encontrado",
  "500": "Error del servidor"
}
```
