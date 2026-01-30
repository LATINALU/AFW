# ATP Scaling Guide v1.0.0

## Descripción General

Esta guía proporciona estrategias y mejores prácticas para escalar ATP (Agentic Task Platform) para manejar alta concurrencia y grandes volúmenes de usuarios.

## Arquitectura de Escalado

### 1. Componentes Clave

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (NGINX)                 │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌──────▼───────┐ ┌───────▼────────┐
│  Backend       │ │  Backend     │ │  Backend       │
│  Instance 1    │ │  Instance 2  │ │  Instance 3    │
└───────┬────────┘ └──────┬───────┘ └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌──────▼───────┐ ┌───────▼────────┐
│  Redis Cache   │ │  PostgreSQL  │ │  Redis Queue   │
│  (Sessions)    │ │  (Database)  │ │  (Tasks)       │
└────────────────┘ └──────────────┘ └────────────────┘
```

## Implementaciones Realizadas

### ✅ 1. Sistema de Tracking de Usuarios en Línea

**Ubicación**: `backend/app/services/online_users_tracker.py`

**Características**:
- Tracking en tiempo real con Redis
- Fallback a memoria si Redis no está disponible
- Detección automática de desconexiones
- Estadísticas de concurrencia y picos

**Uso**:
```python
from app.services.online_users_tracker import get_tracker

tracker = get_tracker()

# Agregar usuario
await tracker.add_user(
    user_id="user123",
    session_id="session_abc",
    client_id="client_xyz",
    device_type="mobile"
)

# Obtener estadísticas
stats = await tracker.get_stats()
print(f"Usuarios en línea: {stats['online_users']}")
```

### ✅ 2. Dashboard de Administración

**Ubicación**: 
- Backend: `backend/app/routes/admin_routes.py`
- Frontend: `frontend/src/components/admin/AdminDashboard.tsx`

**Endpoints Disponibles**:
- `GET /api/admin/stats/online-users` - Usuarios conectados
- `GET /api/admin/stats/system` - Métricas del sistema
- `GET /api/admin/stats/websocket` - Estadísticas WebSocket
- `GET /api/admin/stats/dashboard` - Dashboard completo
- `POST /api/admin/broadcast` - Mensaje broadcast
- `POST /api/admin/users/{user_id}/disconnect` - Desconectar usuario

**Métricas Monitoreadas**:
- Usuarios en línea (actual y pico)
- Sesiones activas
- Uso de CPU y memoria
- Conexiones WebSocket
- Distribución por dispositivo

### ✅ 3. Interfaz Móvil Optimizada

**Ubicación**: `frontend/src/components/mobile/`

**Componentes Creados**:
- `MobileChatInterface.tsx` - Chat optimizado para móvil
- `MobileAgentSelector.tsx` - Selector de agentes táctil
- `MobileBottomNav.tsx` - Navegación inferior
- `MobileLayout.tsx` - Layout principal móvil
- `useDeviceDetection.ts` - Hook de detección de dispositivo

**Características**:
- Gestos táctiles optimizados
- Interfaz adaptativa según tamaño de pantalla
- Componentes específicos para móvil/tablet/desktop
- Animaciones suaves con Framer Motion

### ✅ 4. REST API v1 para Integraciones

**Ubicación**: `backend/app/routes/api_v1_routes.py`

**Autenticación**: API Keys con header `X-API-Key`

**Endpoints Principales**:
- `POST /api/v1/chat` - Chat con agentes
- `GET /api/v1/agents` - Listar agentes
- `GET /api/v1/models` - Listar modelos
- `GET /api/v1/usage` - Estadísticas de uso
- `POST /api/v1/keys/generate` - Generar API key
- `GET /api/v1/keys` - Listar API keys
- `DELETE /api/v1/keys/{key_prefix}` - Revocar API key

**Rate Limiting**:
- Chat: 30 requests/minuto
- Listados: 60 requests/minuto
- Gestión de keys: 10 requests/minuto

### ✅ 5. Sistema de Caché con Redis

**Ubicación**: `backend/app/services/cache_manager.py`

**Características**:
- Caché de respuestas de agentes
- Caché de consultas frecuentes
- TTL configurable por tipo
- Fallback a memoria
- Decorador `@cached` para funciones

**Uso**:
```python
from app.services.cache_manager import get_cache_manager, cached

cache = get_cache_manager()

# Cachear respuesta de agente
await cache.cache_agent_response(
    agent_id="reasoning",
    task="Analizar datos",
    model="gpt-4",
    response="Análisis completo..."
)

# Obtener respuesta cacheada
cached_response = await cache.get_cached_agent_response(
    agent_id="reasoning",
    task="Analizar datos",
    model="gpt-4"
)

# Usar decorador
@cached(ttl=3600)
async def expensive_operation():
    return result
```

## Estrategias de Escalado

### 1. Escalado Horizontal (Recomendado)

**Múltiples Instancias del Backend**:

```bash
# Instancia 1
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4

# Instancia 2
uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 4

# Instancia 3
uvicorn app.main:app --host 0.0.0.0 --port 8003 --workers 4
```

**NGINX Load Balancer**:

```nginx
upstream atp_backend {
    least_conn;
    server backend1:8001 weight=1 max_fails=3 fail_timeout=30s;
    server backend2:8002 weight=1 max_fails=3 fail_timeout=30s;
    server backend3:8003 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name api.atp.com;

    location / {
        proxy_pass http://atp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 2. Optimización de Base de Datos

**PostgreSQL en lugar de SQLite**:

```python
# config.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/atp"
)
```

**Índices Recomendados**:

```sql
-- Índice en usuarios
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Índice en API keys
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);

-- Índice en uso de API
CREATE INDEX idx_api_usage_key_hash ON api_usage(key_hash);
CREATE INDEX idx_api_usage_timestamp ON api_usage(timestamp);
```

### 3. Redis Cluster para Alta Disponibilidad

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-master-data:/data
    command: redis-server --appendonly yes

  redis-replica-1:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    volumes:
      - redis-replica-1-data:/data
    command: redis-server --slaveof redis-master 6379

  redis-replica-2:
    image: redis:7-alpine
    ports:
      - "6381:6379"
    volumes:
      - redis-replica-2-data:/data
    command: redis-server --slaveof redis-master 6379

volumes:
  redis-master-data:
  redis-replica-1-data:
  redis-replica-2-data:
```

### 4. WebSocket Sticky Sessions

Para mantener conexiones WebSocket consistentes:

```nginx
upstream websocket_backend {
    ip_hash;  # Sticky sessions por IP
    server backend1:8001;
    server backend2:8002;
    server backend3:8003;
}

server {
    location /ws/ {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

### 5. CDN para Assets Estáticos

**Vercel/Netlify para Frontend**:
- Distribución global automática
- Cache edge optimizado
- SSL/TLS incluido

**CloudFlare para API**:
- DDoS protection
- Rate limiting adicional
- Cache de respuestas GET

## Monitoreo y Alertas

### Métricas Clave a Monitorear

1. **Usuarios en Línea**:
   - Usuarios actuales
   - Pico de usuarios
   - Distribución por dispositivo

2. **Performance**:
   - Tiempo de respuesta de API
   - Latencia de WebSocket
   - Tasa de errores

3. **Recursos**:
   - CPU usage
   - Memoria usage
   - Conexiones de base de datos
   - Redis memory

4. **Rate Limiting**:
   - Requests por minuto
   - Usuarios bloqueados
   - API keys más activas

### Herramientas Recomendadas

- **Prometheus + Grafana**: Métricas y dashboards
- **Sentry**: Error tracking
- **DataDog**: APM y monitoreo
- **Uptime Robot**: Monitoreo de uptime

## Optimizaciones de Performance

### 1. Caché Agresivo

```python
# Cachear respuestas de agentes por 2 horas
await cache.cache_agent_response(
    agent_id=agent_id,
    task=task,
    model=model,
    response=response
)

# Cachear consultas frecuentes por 30 minutos
await cache.cache_query_result(
    query=query,
    agents=agents,
    model=model,
    result=result
)
```

### 2. Connection Pooling

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### 3. Async Everywhere

```python
# Usar async/await para todas las operaciones I/O
async def process_task(task: str):
    # Operaciones de DB
    user = await db.get_user_async(user_id)
    
    # Operaciones de caché
    cached = await cache.get(key)
    
    # Llamadas a API externa
    result = await llm_client.generate(prompt)
    
    return result
```

### 4. Batch Processing

```python
# Procesar múltiples tareas en paralelo
tasks = [process_task(t) for t in task_list]
results = await asyncio.gather(*tasks)
```

## Límites Recomendados

### Configuración de Producción

```python
# config.py

# Rate Limiting
RATE_LIMIT_CHAT = "30/minute"
RATE_LIMIT_API = "60/minute"
RATE_LIMIT_ADMIN = "100/minute"

# WebSocket
MAX_WEBSOCKET_CONNECTIONS = 10000
WEBSOCKET_TIMEOUT = 300  # 5 minutos

# Database
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 40

# Redis
REDIS_MAX_CONNECTIONS = 50
REDIS_SOCKET_TIMEOUT = 5

# Cache TTLs
AGENT_RESPONSE_TTL = 7200  # 2 horas
QUERY_CACHE_TTL = 1800  # 30 minutos
USER_SESSION_TTL = 86400  # 24 horas
```

## Checklist de Escalado

- [x] Sistema de tracking de usuarios en línea
- [x] Dashboard de administración con métricas
- [x] Interfaz móvil optimizada
- [x] REST API con autenticación
- [x] Sistema de caché con Redis
- [ ] Migrar de SQLite a PostgreSQL
- [ ] Implementar Redis Cluster
- [ ] Configurar load balancer
- [ ] Implementar CDN
- [ ] Configurar monitoreo (Prometheus/Grafana)
- [ ] Implementar logging centralizado
- [ ] Configurar backups automáticos
- [ ] Implementar CI/CD pipeline
- [ ] Configurar auto-scaling

## Próximos Pasos

1. **Migración a PostgreSQL**: Mejor performance para alta concurrencia
2. **Redis Cluster**: Alta disponibilidad del caché
3. **Kubernetes**: Orquestación de contenedores para auto-scaling
4. **Message Queue**: RabbitMQ/Celery para tareas asíncronas
5. **Observabilidad**: Logs estructurados y tracing distribuido

## Soporte

Para más información sobre escalado:
- Documentación: https://docs.atp.com/scaling
- Email: devops@atp.com
- Discord: #scaling-help
