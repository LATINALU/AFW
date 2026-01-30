# Docker Setup Guide v1.0.0
# =====================
# Guía completa para ejecutar ATP localmente con Docker

## 🚀 Inicio Rápido

### 1. Requisitos Previos

```bash
# Docker y Docker Compose
docker --version
docker-compose --version

# O Docker Desktop (incluye ambos)
```

### 2. Ejecutar en Desarrollo

```bash
# Clonar repositorio (si no está clonado)
git clone <repo-url>
cd ATPE

# Ejecutar todo el sistema
docker-compose -f docker-compose.dev.yml up --build
```

### 3. Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Redis**: localhost:6379

---

## 📋 Configuración Completa

### Variables de Entorno

Crear `.env` en la raíz del proyecto:

```bash
# .env
# Backend
ENVIRONMENT=development
DEBUG=true
JWT_SECRET_KEY=atp_dev_secret_key_2024
SESSION_SECRET=atp_dev_session_secret_2024
ENCRYPTION_KEY=atp_dev_encryption_key_2024
API_SECRET_KEY=atp_dev_api_secret_2024

# Redis
REDIS_URL=redis://redis:6379
REDIS_KEY=atp_dev_redis_key_2024

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_VERSION=1.0.0
NEXT_PUBLIC_DEMO_MODE=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
```

### Estructura de Archivos

```
ATPE/
├── docker-compose.dev.yml          # Configuración desarrollo
├── docker-compose.yml              # Configuración producción
├── .env                           # Variables de entorno
├── backend/
│   ├── Dockerfile.dev             # Docker desarrollo backend
│   ├── requirements.txt            # Dependencias Python
│   ├── app/                       # Código backend
│   └── data/                      # Base de datos local
├── frontend/
│   ├── Dockerfile.dev             # Docker desarrollo frontend
│   ├── package.json               # Dependencias Node.js
│   └── src/                       # Código frontend
├── redis.conf                     # Configuración Redis
└── nginx/                         # Configuración NGINX (producción)
```

---

## 🐳 Docker Compose - Desarrollo

### docker-compose.dev.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: atp-backend-dev
    ports:
      - "8001:8001"
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
      - HOST=0.0.0.0
      - PORT=8001
      - PYTHONPATH=/app
      - ENVIRONMENT=development
      - DEBUG=true
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./backend:/app                    # Hot reload
      - ./backend/data:/app/data           # Persistencia DB
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    container_name: atp-redis-dev
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
      args:
        - NEXT_PUBLIC_API_URL=http://localhost:8001
    container_name: atp-frontend-dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - NEXT_PUBLIC_API_URL=http://localhost:8001
    volumes:
      - ./frontend:/app                   # Hot reload
      - /app/node_modules                  # Persistir node_modules
    depends_on:
      backend:
        condition: service_healthy

volumes:
  redis_data:
    driver: local
```

---

## 🔧 Configuración Detallada

### Backend Dockerfile.dev

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements para caché
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dependencias de desarrollo
RUN pip install --no-cache-dir pytest pytest-asyncio black flake8

# Copiar código
COPY . .

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOST=0.0.0.0
ENV PORT=8001
ENV PYTHONPATH=/app
ENV ENVIRONMENT=development
ENV DEBUG=true

EXPOSE 8001

# Hot reload en desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

### Frontend Dockerfile.dev

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar package files para caché
COPY package*.json ./
RUN npm ci

# Instalar dependencias adicionales
RUN npm install -g @tailwindcss/cli

# Copiar código
COPY . .

# Variables de entorno
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000

# Development con hot reload
CMD ["npm", "run", "dev"]
```

---

## 🗄️ Base de Datos y Persistencia

### Directorios de Datos

```bash
# Crear directorios persistentes
mkdir -p backend/data
mkdir -p logs

# Permisos (Linux/Mac)
chmod 755 backend/data
chmod 755 logs
```

### Base de Datos SQLite

La base de datos se crea automáticamente en:
- `backend/data/atp_users.db` - Usuarios y autenticación
- `backend/data/atp_conversations.db` - Conversaciones y mensajes

### Redis Cache

Redis persiste en el volumen `redis_data`:
- Cache de respuestas de agentes
- Sesiones de usuarios
- Rate limiting
- Tracking de usuarios online

---

## 🚀 Comandos Docker

### Iniciar Servicios

```bash
# Iniciar todo (build + run)
docker-compose -f docker-compose.dev.yml up --build

# Iniciar en background
docker-compose -f docker-compose.dev.yml up -d --build

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Logs de servicio específico
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Detener Servicios

```bash
# Detener todo
docker-compose -f docker-compose.dev.yml down

# Detener y eliminar volúmenes
docker-compose -f docker-compose.dev.yml down -v

# Forzar recreación
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

### Mantenimiento

```bash
# Limpiar imágenes no usadas
docker image prune -f

# Limpiar todo (cuidado!)
docker system prune -af

# Ver estado de contenedores
docker-compose -f docker-compose.dev.yml ps

# Entrar a contenedor
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec frontend sh
```

---

## 🔍 Verificación y Testing

### Health Checks

```bash
# Verificar salud de servicios
curl http://localhost:8001/api/health
curl http://localhost:3000

# Verificar Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli ping
```

### API Testing

```bash
# Health check
curl http://localhost:8001/api/health

# Listar agentes
curl http://localhost:8001/api/agents

# Listar modelos
curl http://localhost:8001/api/models

# WebSocket test
wscat -c ws://localhost:8001/ws/test123
```

### Frontend Testing

```bash
# Acceder a la aplicación
open http://localhost:3000

# Verificar conexión con backend
# En browser console:
fetch('/api/health').then(r => r.json()).then(console.log)
```

---

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. "Port already in use"
```bash
# Ver qué usa el puerto
lsof -i :8001
lsof -i :3000
lsof -i :6379

# Matar procesos
kill -9 <PID>

# O usar diferentes puertos
# Editar docker-compose.dev.yml
ports:
  - "8002:8001"  # Backend en 8002
```

#### 2. "Permission denied"
```bash
# Permisos en Linux/Mac
sudo chown -R $USER:$USER backend/data
sudo chmod -R 755 backend/data

# En Windows, ejecutar como Administrator
```

#### 3. "Build failed"
```bash
# Limpiar y reconstruir
docker-compose -f docker-compose.dev.yml down
docker system prune -f
docker-compose -f docker-compose.dev.yml up --build
```

#### 4. "Database locked"
```bash
# Entrar al contenedor backend
docker-compose -f docker-compose.dev.yml exec backend bash

# Verificar base de datos
ls -la /app/data/

# Reiniciar servicio
docker-compose -f docker-compose.dev.yml restart backend
```

#### 5. "Redis connection failed"
```bash
# Verificar Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli ping

# Reiniciar Redis
docker-compose -f docker-compose.dev.yml restart redis
```

### Logs Útiles

```bash
# Logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f

# Logs de backend
docker-compose -f docker-compose.dev.yml logs -f backend

# Logs de frontend
docker-compose -f docker-compose.dev.yml logs -f frontend

# Logs de Redis
docker-compose -f docker-compose.dev.yml logs -f redis
```

---

## 🔄 Desarrollo Workflow

### 1. Desarrollo Local

```bash
# Iniciar servicios
docker-compose -f docker-compose.dev.yml up --build

# Los cambios en código se reflejan automáticamente (hot reload)
# Backend: Python files
# Frontend: React/Next.js files
```

### 2. Debugging

```bash
# Entrar a contenedor backend
docker-compose -f docker-compose.dev.yml exec backend bash

# Ver logs de aplicación
tail -f /app/logs/app.log

# Debug con pdb (en código)
import pdb; pdb.set_trace()
```

### 3. Testing

```bash
# Tests backend
docker-compose -f docker-compose.dev.yml exec backend pytest

# Tests frontend
docker-compose -f docker-compose.dev.yml exec frontend npm test
```

---

## 📊 Monitoreo

### Recursos

```bash
# Estadísticas de contenedores
docker stats

# Uso de disco
docker-compose -f docker-compose.dev.yml exec backend df -h

# Memoria Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli info memory
```

### Logs Estructurados

```bash
# Logs con timestamps
docker-compose -f docker-compose.dev.yml logs -f --timestamps

# Logs de errores
docker-compose -f docker-compose.dev.yml logs backend | grep ERROR
```

---

## 🚀 Producción

Para producción, usar `docker-compose.yml`:

```bash
# Producción con NGINX
docker-compose -f docker-compose.yml up -d --build

# Incluir SSL certificates
# Configurar dominios
# Setear variables de entorno de producción
```

---

## 📞 Soporte

Si tienes problemas:

1. **Verificar logs**: `docker-compose logs`
2. **Reiniciar servicios**: `docker-compose restart`
3. **Limpiar y reconstruir**: `docker-compose down && docker-compose up --build`
4. **Verificar puertos**: `netstat -tulpn | grep :8001`

---

**¡Listo para desarrollar!** 🎉

Con esta configuración tienes:
- ✅ Backend Python con hot reload
- ✅ Frontend Next.js con hot reload  
- ✅ Redis para caché y sesiones
- ✅ Base de datos persistente
- ✅ Health checks automáticos
- ✅ Logs estructurados
- ✅ Desarrollo optimizado
