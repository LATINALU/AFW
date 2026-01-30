# 🐳 ATP v0.6.1 - Docker Setup Guide

## Guía de Ejecución en Docker Local

### 📋 Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Docker Compose v3.8 o superior
- Puertos 3000 y 8001 disponibles

---

## 🚀 Inicio Rápido

### 1. Construir y Ejecutar

```bash
# Desde el directorio raíz de ATP
docker-compose up --build
```

### 2. Acceder a la Aplicación

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **Health Check:** http://localhost:8001/api/health
- **API Docs:** http://localhost:8001/docs

---

## 📦 Servicios

### Backend (Puerto 8001)
- **Imagen:** Python 3.11-slim
- **Framework:** FastAPI + Uvicorn
- **Agentes:** 30 agentes especializados
- **Orchestrator:** LangGraph StateGraph
- **Protocolo:** A2A (Agent-to-Agent)

### Frontend (Puerto 3000)
- **Imagen:** Node 20-alpine
- **Framework:** Next.js 14
- **Características:** 
  - Chat Interface
  - Node Workflow Editor
  - 30 agentes integrados

---

## 🔧 Comandos Útiles

### Iniciar Servicios
```bash
# Iniciar en modo detached (background)
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Detener Servicios
```bash
# Detener contenedores
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores y volúmenes
docker-compose down -v
```

### Reconstruir Servicios
```bash
# Reconstruir sin cache
docker-compose build --no-cache

# Reconstruir y reiniciar
docker-compose up --build -d
```

### Verificar Estado
```bash
# Ver contenedores en ejecución
docker-compose ps

# Ver uso de recursos
docker stats atp-backend atp-frontend
```

### Acceder a Contenedores
```bash
# Acceder al backend
docker exec -it atp-backend bash

# Acceder al frontend
docker exec -it atp-frontend sh

# Ver logs del backend
docker logs atp-backend

# Ver logs del frontend
docker logs atp-frontend
```

---

## 🔍 Troubleshooting

### Puerto ya en uso
```bash
# Verificar qué está usando el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8001

# Cambiar puertos en docker-compose.yml si es necesario
```

### Contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs backend
docker-compose logs frontend

# Verificar health check
docker inspect atp-backend | grep -A 10 Health
```

### Problemas de conexión Backend-Frontend
```bash
# Verificar red Docker
docker network inspect atp_atp-network

# Verificar que backend esté respondiendo
curl http://localhost:8001/api/health
```

### Limpiar todo y empezar de nuevo
```bash
# Detener y limpiar todo
docker-compose down -v
docker system prune -a

# Reconstruir desde cero
docker-compose up --build
```

---

## 🌐 Variables de Entorno

### Backend
```env
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
HOST=0.0.0.0
PORT=8001
PYTHONPATH=/app
```

### Frontend
```env
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 📊 Health Checks

### Backend Health Check
```bash
curl http://localhost:8001/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "version": "0.6.1",
  "models_available": [...],
  "agents_count": 30
}
```

### Frontend Health Check
```bash
curl http://localhost:3000
```

---

## 🔄 Desarrollo con Hot Reload

Para desarrollo con recarga automática:

```yaml
# Modificar docker-compose.yml para desarrollo
services:
  backend:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    volumes:
      - ./backend:/app
  
  frontend:
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
```

---

## 📝 Notas Importantes

1. **Primera ejecución:** La construcción de imágenes puede tardar 5-10 minutos
2. **API Keys:** Configura tus API keys en la interfaz web (⚙️ Configuración)
3. **Persistencia:** Los datos se almacenan en localStorage del navegador
4. **Red Docker:** Los servicios se comunican a través de la red `atp-network`
5. **Volúmenes:** El código se monta como volumen para facilitar desarrollo

---

## 🎯 Verificación Post-Inicio

### 1. Verificar Backend
```bash
curl http://localhost:8001/api/health
curl http://localhost:8001/api/agents
```

### 2. Verificar Frontend
- Abrir http://localhost:3000
- Verificar que cargue la interfaz
- Verificar que muestre los 30 agentes

### 3. Verificar Integración
- Configurar una API key en ⚙️ Configuración
- Seleccionar agentes
- Enviar un mensaje de prueba
- Verificar respuesta

---

## 🐛 Debug Mode

Para ejecutar en modo debug:

```bash
# Backend con logs detallados
docker-compose exec backend python -m pdb app/main.py

# Ver variables de entorno
docker-compose exec backend env

# Ver procesos
docker-compose exec backend ps aux
```

---

## 📚 Estructura de Contenedores

```
ATP Docker Setup
├── atp-backend (Python 3.11)
│   ├── Puerto: 8001
│   ├── Health Check: /api/health
│   └── 30 Agentes Especializados
│
├── atp-frontend (Node 20)
│   ├── Puerto: 3000
│   ├── Next.js 14
│   └── Chat + Node Editor
│
└── atp-network (Bridge)
    └── Comunicación interna
```

---

## ✅ Checklist de Inicio

- [ ] Docker Desktop ejecutándose
- [ ] Puertos 3000 y 8001 libres
- [ ] Ejecutar `docker-compose up --build`
- [ ] Esperar a que ambos servicios estén "healthy"
- [ ] Acceder a http://localhost:3000
- [ ] Configurar API key en ⚙️ Configuración
- [ ] Probar chat con agentes
- [ ] Probar Node Workflow Editor

---

## 🎉 Sistema Listo

Una vez que veas estos mensajes en los logs:

**Backend:**
```
🚀 Agentic Task Platform v0.6.1 iniciando...
📡 Modelos disponibles: [...]
🤖 30 Agentes Especializados con LangGraph y Protocolo A2A
🧠 Sistema de Orquestación con StateGraph
```

**Frontend:**
```
✓ Ready in Xms
○ Local: http://localhost:3000
```

**¡El sistema está listo para usar!** 🎊

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs: `docker-compose logs`
2. Verificar health checks
3. Consultar MIGRATION_v0.6.1.md
4. Revisar ARCHITECTURE.md

---

**ATP v0.6.1 - Sistema de 30 Agentes Especializados**
**Docker Setup - Listo para Producción Local**
