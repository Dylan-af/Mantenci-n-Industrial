# Guía de Deployment - Mantención Industrial

## 🚀 Deployment en Producción

### Prerrequisitos

- Servidor Linux (Ubuntu 20.04 o superior recomendado)
- Python 3.8+
- PostgreSQL (recomendado para producción)
- Nginx o Apache
- Gunicorn

### 1. Configuración del Servidor

#### Instalar dependencias en Ubuntu
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv postgresql postgresql-contrib nginx git
```

#### Crear usuario para la aplicación
```bash
sudo useradd -m -s /bin/bash mantencion
sudo su - mantencion
```

### 2. Clonar y Configurar la Aplicación

```bash
cd /home/mantencion
git clone https://github.com/Dylan-af/Mantenci-n-Industrial.git
cd Mantenci-n-Industrial

# Crear ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary python-decouple
```

### 3. Configurar PostgreSQL

```bash
sudo -u postgres psql
```

En psql:
```sql
CREATE DATABASE mantenccion_db;
CREATE USER mantenccion_user WITH PASSWORD 'contraseña_segura';
ALTER ROLE mantenccion_user SET client_encoding TO 'utf8';
ALTER ROLE mantenccion_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mantenccion_user SET default_transaction_deferrable TO on;
ALTER ROLE mantenccion_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mantenccion_db TO mantenccion_user;
\q
```

### 4. Configurar Django para Producción

Crear `.env` en el directorio raíz:
```bash
DEBUG=False
SECRET_KEY=generar-clave-segura-aqui
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
TIME_ZONE=America/Santiago
LANGUAGE_CODE=es-es

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=mantenccion_db
DB_USER=mantenccion_user
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-app
```

Actualizar `config/settings.py`:
```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
TIME_ZONE = config('TIME_ZONE', default='UTC')
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default='db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# Security Settings para Producción
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

### 5. Preparar la Aplicación

```bash
source venv/bin/activate

# Generar SECRET_KEY segura
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 6. Configurar Gunicorn

Crear `/home/mantencion/Mantenci-n-Industrial/gunicorn_config.py`:
```python
import multiprocessing

bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

Crear archivo de servicio systemd:
`/etc/systemd/system/mantenccion.service`:
```ini
[Unit]
Description=Mantención Industrial Gunicorn
After=network.target

[Service]
User=mantencion
Group=www-data
WorkingDirectory=/home/mantencion/Mantenci-n-Industrial
Environment="PATH=/home/mantencion/Mantenci-n-Industrial/venv/bin"
ExecStart=/home/mantencion/Mantenci-n-Industrial/venv/bin/gunicorn \
    --config /home/mantencion/Mantenci-n-Industrial/gunicorn_config.py \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 7. Configurar Nginx

Crear `/etc/nginx/sites-available/mantenccion`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # Certificados SSL (generar con Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 20M;

    location /static/ {
        alias /home/mantencion/Mantenci-n-Industrial/staticfiles/;
    }

    location /media/ {
        alias /home/mantencion/Mantenci-n-Industrial/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 8. Instalar Certificado SSL

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Activar Servicios

```bash
sudo systemctl enable mantenccion
sudo systemctl start mantenccion

sudo ln -s /etc/nginx/sites-available/mantenccion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
```

### 10. Monitoreo

```bash
# Ver logs de la aplicación
sudo systemctl status mantenccion
sudo journalctl -u mantenccion -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## 📊 Backup y Restore

### Backup de Base de Datos
```bash
pg_dump -U mantenccion_user -d mantenccion_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore de Base de Datos
```bash
psql -U mantenccion_user -d mantenccion_db < backup.sql
```

### Backup de Archivos
```bash
tar -czf mantenccion_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/mantencion/Mantenci-n-Industrial
```

## 🔄 Actualizar Aplicación

```bash
cd /home/mantencion/Mantenci-n-Industrial
source venv/bin/activate

git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

sudo systemctl restart mantenccion
```

## 📈 Optimización en Producción

### 1. Configurar Cache
```python
# En settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Instalar redis
sudo apt-get install redis-server
pip install django-redis
```

### 2. Configurar Celery (para tareas asincrónicas)
```bash
pip install celery redis
```

### 3. Aumentar Límites del Sistema
```bash
# En /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
```

## 🚨 Checklist de Seguridad

- [ ] Cambiar SECRET_KEY en producción
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] SSL/HTTPS habilitado
- [ ] CSRF y CORS configurados
- [ ] Archivos estáticos servidos por Nginx
- [ ] Media servidos por Nginx
- [ ] Backups automáticos configurados
- [ ] Logs monitoreados
- [ ] Firewall configurado
- [ ] Permisos de archivos correctos
- [ ] Actualizaciones de seguridad aplicadas

## 📞 Troubleshooting

### 502 Bad Gateway
```bash
# Verificar si Gunicorn está corriendo
sudo systemctl status mantenccion

# Verificar logs
sudo journalctl -u mantenccion -n 50
```

### Conexión a BD rechazada
```bash
# Verificar credenciales en .env
# Verificar servicio PostgreSQL
sudo systemctl status postgresql

# Verificar conectividad
psql -U mantenccion_user -d mantenccion_db
```

### Archivos estáticos no se cargan
```bash
# Recolectar nuevamente
python manage.py collectstatic --clear --noinput

# Verificar permisos
sudo chown -R www-data:www-data /home/mantencion/Mantenci-n-Industrial/staticfiles
```

## 📚 Referencias

- [Django Production Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
