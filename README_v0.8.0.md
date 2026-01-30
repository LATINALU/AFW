# AFW - Agents For Works

<p align="center">
  <img src="https://img.shields.io/badge/version-0.8.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-production-ready-brightgreen.svg" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-StateGraph-green.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/Next.js-14.2-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/Redis-Cache-red.svg" alt="Redis">
</p>

# 🤖 AFW Platform v0.8.0 - Production Ready

**AFW (Agents For Works)** es una plataforma completa de IA conversacional con **120 agentes especializados** en 12 categorías, streaming en tiempo real, persistencia de conversaciones, sistema de seguridad completo y despliegue Docker optimizado para producción.

## 🎉 Características Principales v0.8.0

✅ **120 Agentes Especializados** - Sistema completo en 12 categorías profesionales  
✅ **Streaming WebSocket** - Respuestas en tiempo real sin latencia  
✅ **Persistencia Completa** - Historial de conversaciones con búsqueda y gestión  
✅ **Sistema de Seguridad v0.8.0** - JWT, rate limiting, encriptación, validación  
✅ **Interfaz Móvil Optimizada** - Responsive design con componentes táctiles  
✅ **Admin Dashboard** - Monitoreo de usuarios y métricas en tiempo real  
✅ **Multi-proveedor LLM** - Groq, OpenAI, Anthropic, modelos locales  
✅ **Docker Production Ready** - Configuración completa con Nginx proxy  

## 🚀 Quick Start

```bash
# Clonar y ejecutar
git clone https://github.com/LATINALU/AFW.git
cd AFW

# Configurar variables de entorno
cp .env.afw.example .env.afw
# Editar .env.afw con tus API keys

# Iniciar todo con Docker
docker-compose -f docker-compose.afw.yml up -d --build

# Acceder a la aplicación
# Frontend: http://localhost:3002
# Backend: http://localhost:8002
# API Docs: http://localhost:8002/docs
```

## 📱 Demo Rápida

1. **Abrir** http://localhost:3002
2. **Seleccionar agentes** - Click en CategorySidebar para elegir hasta 120 agentes
3. **Iniciar conversación** - Streaming en tiempo real con respuestas individuales
4. **Ver historial** - Panel lateral con conversaciones guardadas
5. **Admin dashboard** - http://localhost:8002/admin/dashboard

---

## 🏗️ Arquitectura del Sistema

### Flujo de Arquitectura
```
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌───────────────┐
│  Frontend    │ -> │   Nginx      │ -> │  Next.js      │ -> │  WebSocket    │
│  (Next.js)   │    │   Proxy      │    │  Proxy API    │    │  Manager      │
└──────────────┘    └──────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  Redis       │ -> │  FastAPI     │ -> │ LangGraph     │ -> │ 120 Agents   │
│  Cache       │    │  Backend     │    │  Orchestrator │    │  Cluster      │
└──────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
```

### Componentes Principales

#### Backend (FastAPI + LangGraph)
- **FastAPI v0.8.0**: Servidor principal con seguridad completa
- **LangGraph StateGraph**: Orquestación de agentes con trazabilidad
- **WebSocket Manager**: Streaming en tiempo real
- **Redis Cache**: Rate limiting y sesiones
- **JWT Auth**: Autenticación y autorización

#### Frontend (Next.js 14.2)
- **StreamingChatV2**: Componente principal de chat con WebSocket
- **CategorySidebar**: Navegación de 120 agentes en 12 categorías
- **ConversationSidebar**: Gestión de historial de conversaciones
- **Admin Dashboard**: Monitoreo en tiempo real
- **Responsive Design**: Optimizado para móvil y desktop

---

## 🧬 Catálogo de Agentes (120 perfiles en 12 categorías)

### 💻 Software Development (10 agentes)
`fullstack_developer`, `backend_architect`, `frontend_specialist`, `mobile_developer`, `devops_engineer`, `database_expert`, `security_specialist`, `qa_automation`, `code_reviewer`, `api_architect`

### 📢 Marketing Digital (10 agentes)
`content_strategist`, `seo_specialist`, `social_media_manager`, `email_marketer`, `ppc_specialist`, `brand_strategist`, `analytics_expert`, `copywriter`, `growth_hacker`, `influencer_manager`

### 💰 Finanzas y Contabilidad (10 agentes)
`financial_analyst`, `accountant`, `tax_specialist`, `auditor`, `budget_planner`, `investment_advisor`, `risk_analyst`, `financial_controller`, `treasury_manager`, `compliance_finance`

### ⚖️ Legal y Compliance (10 agentes)
`corporate_lawyer`, `contract_specialist`, `compliance_officer`, `intellectual_property`, `labor_law_expert`, `regulatory_advisor`, `litigation_specialist`, `data_privacy_officer`, `mergers_acquisitions`, `legal_researcher`

### 👥 Recursos Humanos (10 agentes)
`recruiter`, `talent_development`, `compensation_analyst`, `hr_analytics`, `employee_relations`, `onboarding_specialist`, `performance_manager`, `training_coordinator`, `culture_champion`, `workforce_planner`

### 💼 Ventas y Comercial (10 agentes)
`sales_executive`, `account_manager`, `business_development`, `sales_engineer`, `proposal_writer`, `customer_success`, `channel_manager`, `sales_analyst`, `pricing_specialist`, `key_account_manager`

### ⚙️ Operaciones y Logística (10 agentes)
`supply_chain_analyst`, `logistics_coordinator`, `inventory_specialist`, `quality_assurance_ops`, `process_optimizer`, `procurement_specialist`, `warehouse_manager`, `demand_planner`, `vendor_manager`, `lean_specialist`

### 📚 Educación y Capacitación (10 agentes)
`instructional_designer`, `curriculum_developer`, `elearning_specialist`, `training_facilitator`, `assessment_specialist`, `learning_analyst`, `content_curator`, `academic_advisor`, `educational_technologist`, `knowledge_manager`

### 🎨 Creatividad y Diseño (10 agentes)
`creative_director`, `ux_designer`, `ui_designer`, `brand_designer`, `motion_designer`, `illustrator`, `video_producer`, `art_director`, `copywriter_creative`, `three_d_artist`

### 📋 Gestión de Proyectos (10 agentes)
`project_manager`, `scrum_master`, `product_owner`, `program_manager`, `portfolio_manager`, `agile_coach`, `pmo_specialist`, `resource_planner`, `stakeholder_manager`, `change_manager`

### 🛒 Mercado Libre (10 agentes)
`ml_listing_optimizer`, `ml_ads_specialist`, `ml_customer_service`, `ml_reputation_manager`, `ml_pricing_strategist`, `ml_logistics_expert`, `ml_catalog_manager`, `ml_analytics_expert`, `mercadolibre_product_specialist`, `mercadolibre_sales_optimizer`

### 🎥 YouTube (10 agentes)
`yt_content_strategist`, `yt_seo_specialist`, `yt_script_writer`, `yt_thumbnail_designer`, `yt_analytics_expert`, `yt_monetization_expert`, `yt_shorts_specialist`, `yt_community_manager`, `yt_video_editor_advisor`, `yt_growth_strategist`

---

## 🐳 Docker Configuration

### docker-compose.afw.yml
```yaml
services:
  afw-backend:
    build: ./backend
    ports: ["8002:8001"]
    environment:
      - REDIS_URL=redis://afw-redis:6379
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - RATE_LIMIT_ENABLED=true
    depends_on: [afw-redis]

  afw-frontend:
    build: ./frontend
    ports: ["3002:3000"]
    environment:
      - BACKEND_URL=http://afw-backend:8001
      - NEXT_PUBLIC_WS_URL=ws://afw-app.duckdns.org/ws
    depends_on: [afw-backend]

  afw-redis:
    image: redis:7-alpine
    ports: ["6380:6379"]
```

### Variables de Entorno (.env.afw)
```bash
# API Keys para LLMs
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Seguridad
JWT_SECRET_KEY=your_jwt_secret_key
SESSION_SECRET=your_session_secret_key
ENCRYPTION_KEY=your_encryption_key

# Dominio
AFW_DOMAIN=afw-app.duckdns.org
```

---

## 🧱 Estructura del Proyecto

```
AFW/
├── backend/
│   ├── app/
│   │   ├── agents/                 # 120 agentes en 12 categorías
│   │   │   ├── software_development/
│   │   │   ├── marketing/
│   │   │   ├── finance/
│   │   │   ├── legal/
│   │   │   ├── human_resources/
│   │   │   ├── sales/
│   │   │   ├── operations/
│   │   │   ├── education/
│   │   │   ├── creative/
│   │   │   ├── project_management/
│   │   │   ├── mercadolibre/
│   │   │   └── youtube/
│   │   ├── main.py                 # FastAPI server v0.8.0
│   │   ├── orchestrator.py         # LangGraph execution
│   │   ├── websocket_manager.py    # WebSocket streaming
│   │   ├── auth.py                 # JWT authentication
│   │   ├── validators.py           # Security validation
│   │   └── config.py               # Configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Main chat interface
│   │   │   ├── page.mobile.tsx     # Mobile optimized
│   │   │   └── page.desktop.tsx    # Desktop layout
│   │   ├── components/
│   │   │   ├── StreamingChatV2.tsx # Main chat component
│   │   │   ├── CategorySidebar.tsx # Agent navigation
│   │   │   ├── ConversationSidebar.tsx # Chat history
│   │   │   └── AdminDashboard.tsx  # Monitoring
│   │   ├── lib/
│   │   │   └── api.ts              # API client (rutas relativas)
│   │   └── types/
│   │       └── agent.ts            # Type definitions
│   ├── next.config.mjs             # Next.js config con proxy
│   └── package.json
├── docker-compose.afw.yml
├── .env.afw.example
└── deploy-afw.sh                  # Deployment script
```

---

## 🔌 API Endpoints

### REST API
- `GET /api/health` - Health check del sistema
- `GET /api/agents` - Listar todos los 120 agentes
- `GET /api/categories` - Listar 12 categorías
- `POST /api/chat` - Enviar mensaje a agentes
- `GET /api/chat/conversations` - Listar conversaciones
- `GET /api/chat/conversations/{id}` - Obtener conversación
- `DELETE /api/chat/conversations/{id}` - Eliminar conversación

### WebSocket
- `WS /ws/{client_id}` - Streaming en tiempo real

### Ejemplo de uso
```javascript
// Frontend - StreamingChatV2.tsx
const wsUrl = `${wsProtocol}//${window.location.host}/ws/${clientId}`;
const ws = new WebSocket(wsUrl);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleWebSocketMessage(data);
};
```

---

## 🔐 Sistema de Seguridad v0.8.0

### Características de Seguridad
- **JWT Authentication**: Tokens firmados para sesiones
- **Rate Limiting**: Redis-based rate limiting por IP y usuario
- **Input Validation**: Sanitización completa de inputs
- **API Key Encryption**: Encriptación de claves sensibles
- **CORS Restrictive**: Configuración CORS por entorno
- **WebSocket Security**: Autenticación para conexiones WebSocket

### Middleware de Seguridad
```python
# Rate limiting
@limiter.limit("100/minute")
async def chat_endpoint(request: ChatRequest):
    # Validación de input
    validated = validate_message_input(request.message)
    # Procesamiento seguro
    return await process_chat(validated)
```

---

## 🚀 Deployment en Producción

### VPS Deployment
```bash
# 1. Clonar en VPS
git clone https://github.com/LATINALU/AFW.git
cd AFW

# 2. Configurar variables
cp .env.afw.example .env.afw
# Editar con tus API keys y dominio

# 3. Deploy con script
chmod +x deploy-afw.sh
./deploy-afw.sh

# 4. Configurar Nginx (incluido en deploy)
# El script configura Nginx automáticamente
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name afw-app.duckdns.org;

    location / {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
    }

    location /ws {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 📊 Monitoreo y Métricas

### Admin Dashboard Features
- **Usuarios Online**: Conteo en tiempo real
- **Conexiones WebSocket**: Estado de conexiones activas
- **Sesiones Activas**: Métricas de uso
- **Sistema**: CPU, memoria, Redis stats
- **Agentes**: Estadísticas de uso por categoría

### Health Checks
```bash
# Backend health
curl http://localhost:8002/api/health

# Frontend health
curl http://localhost:3002/api/health

# Redis status
docker exec afw-redis redis-cli ping
```

---

## 🧪 Desarrollo Local

### Sin Docker
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Frontend
cd frontend
npm install
npm run dev
```

### Con Docker (Desarrollo)
```bash
# Desarrollo con hot-reload
docker-compose -f docker-compose.dev.yml up
```

---

## 🛠️ Troubleshooting Común

### Problema: /api/api/ duplicación
**Solución**: Usar rutas relativas en frontend (implementado en v0.8.0)
```javascript
// Correcto - ruta relativa
fetchWithAuth("/api/agents");

// Incorrecto - ruta absoluta
fetchWithAuth(`${API_URL}/api/agents`);
```

### Problema: WebSocket no conecta
**Solución**: Verificar configuración Nginx y usar host dinámico
```javascript
const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${wsProtocol}//${window.location.host}/ws/${clientId}`;
```

### Problema: Rate limit excedido
**Solución**: Configurar Redis y ajustar límites
```bash
# Verificar Redis
docker exec afw-redis redis-cli info

# Ajustar rate limit en .env.afw
RATE_LIMIT_REQUESTS_PER_MINUTE=200
```

---

## 🗺️ Roadmap v0.9.0+

### Próximas Versiones
- [ ] **Base de Datos Persistente**: PostgreSQL para conversaciones
- [ ] **Multi-tenant**: Organizaciones y equipos
- [ ] **Agent Marketplace**: Agentes personalizados por usuarios
- [ ] **Voice Chat**: Integración con STT/TTS
- [ ] **File Upload**: Procesamiento de documentos
- [ ] **API v2**: GraphQL y webhooks
- [ ] **Analytics Dashboard**: Métricas avanzadas
- [ ] **Mobile App**: React Native

### Mejoras Técnicas
- [ ] **Testing E2E**: Suite completa con Playwright
- [ ] **CI/CD Pipeline**: GitHub Actions
- [ ] **Kubernetes**: Despliegue en K8s
- [ ] **Microservices**: Arquitectura distribuida
- [ ] **Caching**: Redis Cluster
- [ ] **Monitoring**: Prometheus + Grafana

---

## 🤝 Contribuir

1. **Fork** el repositorio
2. **Crear rama**: `feature/nueva-funcionalidad`
3. **Commits descriptivos**: `feat: agregar agente de X`
4. **Pull Request**: Seguir template de PR
5. **Tests**: Asegurar que todo funciona

### Guidelines
- **Código**: Seguir PEP 8 (Python) y ESLint (TypeScript)
- **Commits**: Usar Conventional Commits
- **Documentación**: Actualizar README y docs
- **Tests**: Unit tests para nuevas features

---

## 📝 Licencia

MIT © LATINALU – Uso libre para proyectos personales y comerciales.

**Atribución requerida**: Por favor, enlaza este repositorio cuando reutilices componentes esenciales.

---

## 📞 Contacto y Soporte

- **Issues**: [GitHub Issues](https://github.com/LATINALU/AFW/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LATINALU/AFW/discussions)
- **Email**: support@afw-platform.com
- **Demo**: https://afw-app.duckdns.org

---

**AFW v0.8.0** - La plataforma más completa de agentes especializados con streaming en tiempo real.
