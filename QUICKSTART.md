# 🚀 Guía Rápida de Inicio

## ⚡ Inicio Rápido (5 minutos)

### 1. Activar Ambiente Virtual
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 2. Ejecutar Servidor
```bash
python manage.py runserver
```

### 3. Acceder a la API
- **Raíz API:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/
  - Usuario: `admin`
  - Contraseña: (la que configuraste)

---

## 📱 Primeros Pasos en la API

### 1. Crear una Empresa
```bash
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"MiEmpresa","rut":"12.345.678-9","email":"info@empresa.cl"}' \
  -u admin:contraseña
```

### 2. Ver la Empresa Creada
```bash
curl http://127.0.0.1:8000/api/empresas/1/
```

### 3. Crear un Equipo
```bash
curl -X POST http://127.0.0.1:8000/api/equipos/ \
  -H "Content-Type: application/json" \
  -d '{"empresa":1,"nombre":"Bomba","codigo":"EQ-001","tipo":"Bomba"}' \
  -u admin:contraseña
```

### 4. Listar todos los Equipos
```bash
curl http://127.0.0.1:8000/api/equipos/
```

---

## 🔧 Comandos Esenciales

| Comando | Descripción |
|---------|-------------|
| `python manage.py runserver` | Ejecutar servidor desarrollo |
| `python manage.py shell` | Acceder shell de Django |
| `python manage.py migrate` | Aplicar migraciones |
| `python manage.py createsuperuser` | Crear usuario admin |
| `python manage.py makemigrations` | Crear nuevas migraciones |
| `python manage.py check` | Verificar configuración |

---

## 📚 Documentación

- **API Completa:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Ejemplos:** [API_EXAMPLES.md](./API_EXAMPLES.md)
- **Deployment:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **README:** [README.md](./README.md)

---

## 🔐 Autenticación

**Para crear/editar/eliminar (POST, PUT, PATCH, DELETE):**

Usar `-u admin:contraseña` con curl:
```bash
curl -X POST ... -u admin:contraseña
```

O ingresar manualmente en http://127.0.0.1:8000/api-auth/login/

---

## 📊 Endpoints Principales

### Empresas
- `GET /api/empresas/` - Listar
- `POST /api/empresas/` - Crear
- `GET /api/empresas/{id}/` - Detalles
- `GET /api/empresas/{id}/estadisticas/` - Estadísticas

### Equipos
- `GET /api/equipos/` - Listar
- `POST /api/equipos/` - Crear
- `GET /api/equipos/operativos/` - Solo operativos
- `GET /api/equipos/{id}/estadisticas/` - Estadísticas

### Técnicos
- `GET /api/tecnicos/` - Listar
- `POST /api/tecnicos/` - Crear
- `GET /api/tecnicos/disponibles/` - Solo activos

### Planes
- `GET /api/planes/` - Listar
- `POST /api/planes/` - Crear
- `GET /api/planes/activos/` - Solo activos

### Órdenes
- `GET /api/ordenes/` - Listar
- `POST /api/ordenes/` - Crear
- `POST /api/ordenes/{id}/iniciar/` - Iniciar
- `POST /api/ordenes/{id}/completar/` - Completar

---

## ⚙️ Configuración Inicial Necesaria

1. ✅ **Ambiente virtual** - Ya creado
2. ✅ **Dependencias** - Ya instaladas
3. ✅ **Base de datos** - Ya migrada
4. ✅ **Superusuario** - Ya creado

**Solo falta:** Ejecutar `python manage.py runserver` y comenzar a usar

---

## 💡 Ejemplos Comunes

### Crear Empresa
```json
{
  "nombre": "Minería XYZ",
  "rut": "78.123.456-7",
  "email": "contacto@mineria.cl",
  "telefono": "+56912345678",
  "ciudad": "Antofagasta"
}
```

### Crear Equipo
```json
{
  "empresa": 1,
  "nombre": "Compresor Industrial",
  "codigo": "EQ-001",
  "tipo": "Compresor",
  "marca": "Atlas Copco",
  "estado": "operativo"
}
```

### Crear Técnico
```json
{
  "nombre": "Juan",
  "apellido": "García",
  "rut": "18.123.456-7",
  "email": "juan@tecnico.cl",
  "telefono": "+56912345678",
  "especialidad": "mecanico",
  "experiencia_anos": 5
}
```

### Crear Plan
```json
{
  "empresa": 1,
  "equipo": 1,
  "nombre": "Mantenimiento Mensual",
  "tipo": "preventivo",
  "frecuencia": "mensual",
  "duracion_estimada_horas": 2.5,
  "tareas": "Revisar, limpiar, cambiar aceite",
  "fecha_inicio": "2025-12-01"
}
```

### Crear Orden
```json
{
  "empresa": 1,
  "equipo": 1,
  "plan": 1,
  "tecnico_asignado": 1,
  "descripcion": "Mantenimiento programado",
  "estado": "programada",
  "prioridad": "media",
  "fecha_programada": "2025-12-18T10:00:00Z"
}
```

---

## 🐛 Solucionar Problemas Comunes

### "ModuleNotFoundError: No module named 'django'"
```bash
# Activar ambiente virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### "Database error"
```bash
python manage.py migrate
```

---

## 📞 Soporte

- Documentación: Ver carpeta actual
- Issues: https://github.com/Dylan-af/Mantenci-n-Industrial/issues
- Email: dylan.merino@incapmail.cl

---

## ✅ Checklist

- [ ] Clonar repositorio
- [ ] Crear ambiente virtual
- [ ] Instalar dependencias
- [ ] Migrar base de datos
- [ ] Crear superusuario
- [ ] Ejecutar servidor
- [ ] Acceder a http://127.0.0.1:8000/
- [ ] Probar endpoints
- [ ] Crear datos de prueba

---

**¡Listo! Ya puedes comenzar a usar la API de Mantención Industrial**
