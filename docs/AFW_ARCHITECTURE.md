# 🏗️ AFW v0.5.0 - Arquitectura del Sistema

> **Agents For Works** - Arquitectura Escalable para el Desarrollo de la Humanidad

## 📐 Visión General

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AFW Platform v0.5.0                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │   Frontend  │◄──►│   Backend   │◄──►│   Agents    │                  │
│  │  (Next.js)  │    │  (FastAPI)  │    │  (102 AI)   │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
│         │                  │                  │                          │
│         ▼                  ▼                  ▼                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │  EldoraUI   │    │  Database   │    │  LangGraph  │                  │
│  │  Components │    │  (SQLite)   │    │  A2A Proto  │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Principios de Arquitectura

### 1. **Modularidad**
- Cada agente es un módulo independiente
- Categorías organizan agentes por dominio
- Fácil agregar/remover agentes sin afectar el sistema

### 2. **Escalabilidad**
- Diseño horizontal para múltiples instancias
- Límites configurables (10 agentes/tarea, 102 total)
- Cache con Redis para alta concurrencia

### 3. **Extensibilidad**
- Protocol A2A para comunicación entre agentes
- Workflows pre-programados reutilizables
- Sistema de plugins para nuevas categorías

---

## 📁 Estructura del Proyecto

```
AFW/
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 agents/                    # 102 Agentes Especializados
│   │   │   ├── 📂 categories/            # 10 Categorías
│   │   │   │   ├── 📂 software_development/  (10 agentes)
│   │   │   │   ├── 📂 marketing/             (12 agentes) ⭐ +2 ML
│   │   │   │   ├── 📂 finance/               (10 agentes)
│   │   │   │   ├── 📂 legal/                 (10 agentes)
│   │   │   │   ├── 📂 human_resources/       (10 agentes)
│   │   │   │   ├── 📂 sales/                 (10 agentes)
│   │   │   │   ├── 📂 operations/            (10 agentes)
│   │   │   │   ├── 📂 education/             (10 agentes)
│   │   │   │   ├── 📂 creative/              (10 agentes)
│   │   │   │   └── 📂 project_management/    (10 agentes)
│   │   │   ├── base_agent.py             # Clase base para todos
│   │   │   ├── agent_registry.py         # Registro singleton
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📂 workflows/                 # 50 Workflows Pre-programados
│   │   │   ├── base_workflow.py          # Clases base
│   │   │   ├── workflow_registry.py      # Registro de workflows
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📂 api/                       # Endpoints REST
│   │   │   ├── routes/
│   │   │   └── middleware/
│   │   │
│   │   ├── afw_config.py                 # Configuración central
│   │   └── main.py                       # Entry point
│   │
│   ├── 📂 src/
│   │   └── 📂 shared/
│   │       └── a2a_protocol.py           # Protocolo Agent-to-Agent
│   │
│   └── requirements.txt
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/                # Componentes React
│   │   │   ├── StreamingChatV2.tsx       # Chat principal
│   │   │   └── ui/                       # EldoraUI components
│   │   ├── 📂 lib/                       # Utilidades
│   │   │   ├── conversationStorage.ts
│   │   │   ├── userStorage.ts
│   │   │   └── encryption.ts
│   │   └── 📂 styles/                    # Estilos globales
│   │
│   ├── package.json
│   └── tailwind.config.js
│
├── 📂 docs/                              # Documentación
│   ├── AFW_AGENTS_CATALOG.md             # Catálogo de 102 agentes
│   ├── AFW_ARCHITECTURE.md               # Este archivo
│   └── AFW_DEVELOPER_GUIDE.md            # Guía de desarrollo
│
└── 📂 docker/                            # Containerización
    ├── docker-compose.yml
    └── Dockerfile
```

---

## 🔄 Flujo de Datos

### 1. Request Flow
```
Usuario → Frontend → API Gateway → Agent Router → Agent(s) → Response
```

### 2. Agent Communication (A2A Protocol)
```
Agent A ──► Message Queue ──► Agent B
    │                            │
    └──── Shared Context ────────┘
```

### 3. Workflow Execution
```
WorkflowTemplate → Steps[] → Agent Assignment → Parallel/Sequential Execution
```

---

## 🧩 Componentes Principales

### Backend (FastAPI)

| Componente | Descripción | Archivo |
|------------|-------------|---------|
| **Agent Registry** | Singleton que gestiona 102 agentes | `agent_registry.py` |
| **Workflow Registry** | 50 workflows pre-programados | `workflow_registry.py` |
| **Base Agent** | Clase abstracta para todos los agentes | `base_agent.py` |
| **A2A Protocol** | Comunicación entre agentes | `a2a_protocol.py` |
| **Config** | Configuración centralizada | `afw_config.py` |

### Frontend (React/Next.js)

| Componente | Descripción | Archivo |
|------------|-------------|---------|
| **StreamingChat** | Interfaz de chat con streaming | `StreamingChatV2.tsx` |
| **Agent Selector** | Selección de hasta 10 agentes | `AgentSelector.tsx` |
| **Conversation Storage** | Persistencia local | `conversationStorage.ts` |

---

## ⚙️ Configuración

### Límites del Sistema

```python
# afw_config.py
AFW_VERSION = "0.5.0"
AFW_NAME = "Agents For Works"

# Límites de agentes
MAX_AGENTS_PER_TASK = 10      # Máximo por tarea
TOTAL_AGENTS = 102            # Total disponibles

# Categorías
AGENT_CATEGORIES = [
    "software_development",
    "marketing",           # 12 agentes (incluye Mercado Libre)
    "finance",
    "legal",
    "human_resources",
    "sales",
    "operations",
    "education",
    "creative",
    "project_management"
]
```

---

## 🚀 Escalabilidad

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
services:
  backend:
    replicas: 3
    
  redis:
    image: redis:alpine
    
  nginx:
    load_balancer: round_robin
```

### Vertical Scaling
- Más agentes por categoría
- Workflows más complejos
- Mayor contexto por agente

---

## 🔐 Seguridad

### Autenticación
- JWT tokens para API
- Session management con Redis
- Encriptación AES-GCM para datos sensibles

### Storage Keys (Frontend)
```typescript
const STORAGE_PREFIX = 'afw_';  // Prefijo para localStorage
// afw_conversations, afw_token, afw_user, etc.
```

---

## 📈 Métricas y Monitoreo

### KPIs del Sistema
- Tiempo de respuesta por agente
- Tasa de éxito de workflows
- Uso de tokens por tarea
- Agentes más utilizados

### Logging
```python
# Cada agente tiene logging integrado
logger.info(f"Agent {agent_id} processing task")
logger.debug(f"Context: {context}")
```

---

## 🔄 Ciclo de Vida de un Agente

```
1. Registration    → AgentRegistry.register()
2. Initialization  → __init__(model, api_config)
3. Processing      → process(input) / get_system_prompt()
4. Communication   → A2A Protocol (si colabora)
5. Response        → Structured output
```

---

## 🛣️ Roadmap de Arquitectura

### v0.6.0
- [ ] Microservicios para categorías
- [ ] Event-driven architecture
- [ ] GraphQL API

### v0.7.0
- [ ] Multi-tenancy
- [ ] Real-time collaboration
- [ ] Agent marketplace

### v1.0.0
- [ ] Self-healing agents
- [ ] Auto-scaling
- [ ] Global distribution

---

## 📊 Diagrama de Clases (Simplificado)

```
┌──────────────────┐
│    BaseAgent     │ (Abstract)
├──────────────────┤
│ - agent_id       │
│ - name           │
│ - capabilities   │
├──────────────────┤
│ + process()      │
│ + get_prompt()   │
└────────┬─────────┘
         │
         ├──────────────────────────────────────┐
         │                                      │
┌────────▼─────────┐              ┌─────────────▼──────────────┐
│ SEOSpecialist    │              │ MercadoLibreProductSpec    │
├──────────────────┤              ├────────────────────────────┤
│ + seo_audit()    │              │ + generate_tech_sheet()    │
│ + keywords()     │              │ + ml_attributes()          │
└──────────────────┘              └────────────────────────────┘
```

---

## 🎯 Decisiones de Diseño

| Decisión | Razón |
|----------|-------|
| **Singleton para Registries** | Garantiza única fuente de verdad |
| **Decoradores para registro** | Código más limpio y declarativo |
| **10 agentes por categoría** | Balance entre especialización y mantenibilidad |
| **Workflows pre-programados** | Automatización de tareas comunes |
| **LocalStorage con prefijo** | Aislamiento de datos entre versiones |

---

*Arquitectura AFW v0.5.0 - Diseñada para escalar*
