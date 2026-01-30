# 🚀 VPS Multi-Project Setup Guide
## Ubuntu 24.04 - 147.93.191.92

## 📁 Estructura de Directorios Propuesta

```
/root/
├── projects/                    # Directorio principal para todos los proyectos
│   ├── atp-platform/          # Proyecto ATP Platform
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── docker-compose.yml
│   │   ├── .env
│   │   └── README.md
│   ├── project2/               # Nuevo proyecto 2
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── docker-compose.yml
│   │   └── .env
│   └── project3/               # Nuevo proyecto 3
│       ├── api/
│       ├── web/
│       ├── docker-compose.yml
│       └── .env
├── databases/                   # Directorio para bases de datos
│   ├── postgres/
│   │   ├── data/
│   │   ├── docker-compose.yml
│   │   └── .env
│   ├── mysql/
│   │   ├── data/
│   │   ├── docker-compose.yml
│   │   └── .env
│   └── mongodb/
│       ├── data/
│       ├── docker-compose.yml
│       └── .env
├── nginx/                      # Configuración Nginx (reverse proxy)
│   ├── nginx.conf
│   ├── sites-available/
│   │   ├── atp-app.duckdns.org.conf
│   │   ├── project2.conf
│   │   └── project3.conf
│   └── ssl/
├── ssl/                        # Certificados SSL
│   ├── atp-app.duckdns.org/
│   └── project2/
├── backups/                    # Directorio para backups
│   ├── databases/
│   └── projects/
├── scripts/                    # Scripts de automatización
│   ├── setup-project.sh
│   ├── backup.sh
│   └── deploy.sh
├── logs/                       # Logs de todos los proyectos
│   ├── atp-platform/
│   ├── project2/
│   └── nginx/
└── monitoring/                 # Configuración de monitoreo
    ├── prometheus/
    └── grafana/
```

## 🔧 Comandos de Limpieza y Configuración Inicial

### 1. Limpieza Completa del VPS
```bash
# SSH al VPS
ssh root@147.93.191.92

# Detener y eliminar todos los contenedores
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Limpiar imágenes y volúmenes
docker system prune -af
docker volume prune -f

# Eliminar directorios antiguos
rm -rf /root/ATPE*
rm -rf /root/projects
rm -rf /root/databases
rm -rf /root/nginx
rm -rf /root/ssl
rm -rf /root/backups
rm -rf /root/scripts
rm -rf /root/logs
rm -rf /root/monitoring

# Recrear estructura de directorios
mkdir -p /root/projects
mkdir -p /root/databases/{postgres,mysql,mongodb}
mkdir -p /root/nginx/{sites-available,ssl}
mkdir -p /root/ssl
mkdir -p /root/backups/{databases,projects}
mkdir -p /root/scripts
mkdir -p /root/logs
mkdir -p /root/monitoring/{prometheus,grafana}
```

### 2. Instalación Base
```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar herramientas esenciales
apt install -y docker.io docker-compose git curl wget unzip nginx certbot python3-certbot-nginx

# Habilitar Docker
systemctl enable docker
systemctl start docker

# Instalar Docker Compose Plugin
apt install -y docker-compose-plugin

# Configurar firewall
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3000/tcp  # Frontend (ejemplo)
ufw allow 8001/tcp  # Backend (ejemplo)
ufw allow 5432/tcp  # PostgreSQL
ufw allow 3306/tcp  # MySQL
ufw allow 27017/tcp # MongoDB
ufw enable
```

## 📝 Scripts de Automatización

### Script: setup-project.sh
```bash
#!/bin/bash
# /root/scripts/setup-project.sh

PROJECT_NAME=$1
PROJECT_TYPE=$2
DOMAIN=$3

if [ -z "$PROJECT_NAME" ]; then
    echo "Uso: ./setup-project.sh <nombre-proyecto> <tipo> [dominio]"
    echo "Tipos: webapp, api, database"
    exit 1
fi

echo "🚀 Configurando proyecto: $PROJECT_NAME"

# Crear directorio del proyecto
PROJECT_DIR="/root/projects/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR/{frontend,backend,database,nginx,logs}"

# Crear docker-compose básico
cat > "$PROJECT_DIR/docker-compose.yml" << EOF
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - NODE_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  database:
  image: postgres:15
  environment:
    POSTGRES_DB: $PROJECT_NAME
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: secure_password_123
  volumes:
    - /root/databases/postgres/$PROJECT_NAME:/var/lib/postgresql/data
  restart: unless-stopped

networks:
  default:
    driver: bridge
EOF

# Crear .env
cat > "$PROJECT_DIR/.env" << EOF
# $PROJECT_NAME Environment Variables
NODE_ENV=production
DOMAIN=$DOMAIN
DATABASE_URL=postgresql://admin:secure_password_123@database:5432/$PROJECT_NAME
EOF

echo "✅ Proyecto $PROJECT_NAME configurado en $PROJECT_DIR"
echo "📝 Editar los archivos en $PROJECT_DIR antes de ejecutar: docker-compose up -d"
```

### Script: deploy.sh
```bash
#!/bin/bash
# /root/scripts/deploy.sh

PROJECT_NAME=$1
DOMAIN=$2

if [ -z "$PROJECT_NAME" ]; then
    echo "Uso: ./deploy.sh <nombre-proyecto> <dominio>"
    exit 1
fi

PROJECT_DIR="/root/projects/$PROJECT_NAME"

echo "🚀 Desplegando $PROJECT_NAME en $DOMAIN"

# Navegar al proyecto
cd "$PROJECT_DIR"

# Build y deploy
docker-compose down
docker-compose build
docker-compose up -d

# Configurar Nginx
cat > /root/nginx/sites-available/$DOMAIN.conf << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Habilitar sitio
ln -sf /root/nginx/sites-available/$DOMAIN.conf /etc/nginx/sites-enabled/

# Recargar Nginx
nginx -t && systemctl reload nginx

echo "✅ $PROJECT_NAME desplegado en http://$DOMAIN"
```

## 🌐 Configuración Nginx Principal

### /root/nginx/nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Include sites
    include /etc/nginx/conf.d/*.conf;
    include /root/nginx/sites-enabled/*.conf;

    # Default server
    server {
        listen 80 default_server;
        server_name _;
        return 444;
    }
}
```

## 📊 Gestión de Bases de Datos

### PostgreSQL Global
```bash
# /root/databases/postgres/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: projects_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secure_password_123
    volumes:
      - ./data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@vps.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    depends_on:
      - postgres
    restart: unless-stopped

networks:
  default:
    driver: bridge
```

## 🔍 Monitoreo

### Prometheus + Grafana
```bash
# /root/monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:

networks:
  default:
    driver: bridge
```

## 📋 Flujo para Agregar Nuevos Proyectos

### 1. Crear Proyecto
```bash
cd /root/scripts
./setup-project.sh mi-nuevo-proyecto webapp midominio.duckdns.org
```

### 2. Configurar Proyecto
```bash
cd /root/projects/mi-nuevo-proyecto
# Editar frontend/, backend/, docker-compose.yml, .env
```

### 3. Desplegar
```bash
cd /root/scripts
./deploy.sh mi-nuevo-proyecto midominio.duckdns.org
```

### 4. Configurar SSL (opcional)
```bash
certbot --nginx -d midominio.duckdns.org
```

## 🔄 Backup Automático

### Script: backup.sh
```bash
#!/bin/bash
# /root/scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backups"

# Backup bases de datos
docker exec postgres pg_dump -U admin projects_db > "$BACKUP_DIR/databases/postgres_$DATE.sql"

# Backup proyectos
for project in /root/projects/*; do
    if [ -d "$project" ]; then
        tar -czf "$BACKUP_DIR/projects/$(basename $project)_$DATE.tar.gz" -C /root/projects $(basename $project)
    fi
done

echo "✅ Backup completado: $DATE"
```

### Cron Job
```bash
# Editar crontab
crontab -e

# Agregar:
0 2 * * * /root/scripts/backup.sh
```

## 🌐 Accesos y Puertos

| Servicio | Puerto | URL |
|---------|-------|-----|
| Nginx | 80/443 | http://147.93.191.92 |
| Proyecto Frontend | 3000 | http://147.93.191.92:3000 |
| Proyecto Backend | 8001 | http://147.93.191.92:8001 |
| PostgreSQL | 5432 | localhost:5432 |
| PgAdmin | 5050 | http://147.93.191.92:5050 |
| Prometheus | 9090 | http://147.93.191.92:9090 |
| Grafana | 3001 | http://147.93.191.92:3001 |

## 🎯 Resumen Final

Tu VPS quedará estructurado para:
- ✅ **Múltiples proyectos** en `/root/projects/`
- ✅ **Bases de datos centralizadas** en `/root/databases/`
- ✅ **Reverse proxy Nginx** para dominios
- ✅ **SSL automático** con Let's Encrypt
- ✅ **Monitoreo** con Prometheus/Grafana
- ✅ **Backups automáticos**
- ✅ **Scripts de automatización**

**¡Listo para desplegar múltiples proyectos! 🚀**
