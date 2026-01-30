# AFW - Agents For Works

<p align="center">
  <img src="https://img.shields.io/badge/version-0.5.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-production-ready-brightgreen.svg" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-StateGraph-green.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/Next.js-14.2-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
</p>

# 🤖 AFW Platform v0.5.0 - Production Ready

**AFW (Agents For Works)** es una plataforma completa de IA conversacional con **100 agentes especializados** en 10 categorías, **50 workflows pre-programados**, persistencia de conversaciones estilo ChatGPT/Gemini, guardado de respuestas individuales, interfaz móvil optimizada y monitoreo en tiempo real.

## 🎉 Características Principales

✅ **Sistema de Persistencia Completo** - Historial de conversaciones con búsqueda  
✅ **Guardado de Respuestas Individuales** - Botón 💾 en cada respuesta de agente  
✅ **Interfaz Móvil Optimizada** - Texto legible y componentes táctiles  
✅ **Admin Dashboard** - Monitoreo de usuarios en tiempo real  
✅ **REST API v1** - Para integraciones externas  
✅ **Alta Concurrency** - Soporte para 1000+ usuarios simultáneos  
✅ **Docker Ready** - Configuración completa para desarrollo y producción  

## 🚀 Quick Start

```bash
# Clonar y ejecutar
git clone <repo-url>
cd AFW

# Iniciar todo con Docker
./RUN_DOCKER.sh  # Linux/Mac
# o
.\RUN_DOCKER.bat  # Windows

# Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

## 📱 Demo Rápida

1. **Abrir** http://localhost:3000
2. **Iniciar conversación** - Se guarda automáticamente
3. **Guardar respuestas** - Click en 💾 en cada respuesta
4. **Ver historial** - Sidebar estilo ChatGPT
5. **Admin dashboard** - http://localhost:8001/admin/dashboard

---

## 🚀 Highlights Clave

| Área | Novedades |
|------|-----------|
| **Chat en Tiempo Real** | Streaming WebSocket para respuestas instantáneas, mensajes individuales por agente con identificación visual (emojis) y auto-scroll. |
| **100 Agentes Funcionales** | Sistema completo de agentes especializados en 10 categorías profesionales, hasta 10 agentes por tarea. |
| **Memoria Contextual** | Persistencia de conversaciones en localStorage, panel de memoria con exportación/importación y continuidad entre sesiones. |
| **Orquestación LangGraph** | Backend FastAPI con StateGraph, agentes aislados y trazabilidad completa de ejecuciones (`✅/❌`). |
| **Docker Ready** | Un único `docker-compose.yml` levanta frontend (Next.js 14.2) y backend (FastAPI) con hot-reload. |

---

## 🧬 Arquitectura de Chat (LangGraph + WebSocket)

```
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌───────────────┐
│  User Query  │ -> │  WebSocket   │ -> │ LangGraph     │ -> │ Agents Cluster │
└──────────────┘    └──────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│Streaming     │ -> │ Individual   │ -> │  Memory Store │ -> │ Frontend UI  │
│Responses     │    │Agent Messages│    │   (localStorage)│  │              │
└──────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
```

El flujo prioriza la experiencia en tiempo real con streaming WebSocket directo al frontend, almacenamiento persistente y respuestas individuales por agente.

---

## 💬 Chat Interface

- **Streaming en Tiempo Real:** WebSocket para respuestas instantáneas sin latencia.
- **Mensajes Individuales:** Cada agente muestra su respuesta por separado con headers visuales (emoji + nombre).
- **Selección de Agentes:** Interfaz simplificada con contador visible (`✓ X / 100 activos`).
- **Memoria Persistente:** Conversaciones guardadas en localStorage con panel de gestión.
- **Auto-scroll:** Scroll automático a nuevos mensajes para mejor UX.
- **Exportación/Importación:** Posibilidad de guardar y cargar conversaciones.

---

## 👥 Catálogo de Agentes (100 perfiles en 10 categorías)

### 💻 Desarrollo de Software (10 agentes)
`tech_lead`, `backend_architect`, `frontend_specialist`, `fullstack_developer`, `mobile_developer`, `devops_engineer`, `database_expert`, `security_specialist`, `qa_automation`, `code_reviewer`

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

Cada agente cuenta con su propio módulo en `backend/app/agents/categories/` y comparte una clase base `BaseAgent` con tracing, logging y configuración de modelo/API.

---

## 🐳 Getting Started con Docker

### Requisitos
- Docker Desktop / Podman
- Python 3.11+ (solo si quieres ejecutar localmente sin contenedores)
- Una API Key de **Groq** (modelo principal: `llama-3.3-70b-versatile`)

### Pasos
```bash
# 1. Clonar el proyecto
git clone https://github.com/LATINALU/AFW.git
cd AFW

# 2. Configurar variables (usa el template actualizado)
copy .env.example .env  # Windows
# edit .env y establece GROQ_API_KEY=tu_api_key_de_groq

# 3. Levantar todo el stack
docker-compose up -d --build

# Backend → http://localhost:8001/api/health
# Frontend → http://localhost:3000
```

> El backend monta el código como volumen (`./backend:/app`), por lo que cualquier cambio se refleja sin reconstruir la imagen. El frontend se sirve en modo producción (Next.js 14.2).

---

## 🧱 Estructura de Carpetas

```
AFW/
├── backend/
│   ├── app/
│   │   ├── agents/                 # 100 agentes especializados en 10 categorías
│   │   ├── orchestrator.py         # LangGraph + WebSocket executor
│   │   ├── main.py                 # FastAPI endpoints (/api/chat, /api/health, WebSocket)
│   │   └── config.py               # Defaults (Groq models, CORS, WebSocket)
│   └── requirements.txt
├── frontend/
│   ├── src/app/page.tsx            # Chat Architecture con StreamingChatV2
│   ├── src/components/             # UI system (StreamingChatV2, MemoryPanel, AgentSelector…)
│   └── package.json                # Next.js 14.2, React 18, Tailwind
├── docker-compose.yml
├── README.md
└── docs/
    ├── PROJECT_OVERVIEW.md
    ├── CHANGELOG_v0.7.2.md
    └── CONFIGURACION_API.md
```

---

## 🔌 API Principal

### `POST /api/chat`
```json
{
  "message": "Describe la arquitectura del sistema.",
  "agents": ["reasoning", "synthesis", "documentation"],
  "model": "llama-3.3-70b-versatile",
  "apiConfig": { "id": "groq", "api_key": "...", "base_url": "https://api.groq.com/openai/v1" }
}
```
Respuesta:
```json
{
  "success": true,
  "result": "Texto final.",
  "agents_used": ["reasoning", "synthesis", "documentation"],
  "model_used": "llama-3.3-70b-versatile",
  "error": null
}
```

### WebSocket `/ws`
Conexión WebSocket para streaming en tiempo real de respuestas individuales de cada agente.

> **Nota:** Si el usuario no aporta `apiConfig`, el backend usa las credenciales Groq definidas en `backend/app/config.py`.

---

## 🧪 Desarrollo Local (sin Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Frontend
cd frontend
npm install
npm run dev
```

Asegúrate de exponer `GROQ_API_KEY` en tu entorno antes de iniciar el backend.

---

## 🗺️ Roadmap
- [ ] **Persistencia Backend:** Mover memoria de localStorage a base de datos (PostgreSQL/MongoDB).
- [ ] **Multi-proveedor:** Integración con OpenAI, Anthropic, Claude vía configuración dinámica.
- [ ] **Testing E2E:** Suite completa con Playwright para garantizar calidad.
- [ ] **Node Workflow:** Re-implementación del editor visual de flujos.
- [ ] **Agentes Personalizados:** Sistema para que usuarios definan sus propios agentes.

---

## 🤝 Contribuir
1. Haz fork del repo.
2. Crea una rama descriptiva (`feature/streaming-chat`).
3. Envía un PR siguiendo la arquitectura actual (WebSocket + LangGraph).

Sugerencias bienvenidas: bugs, mejoras de UI, nuevos agentes, optimización de streaming, etc.

---

## 📝 Licencia
MIT © LATINALU – uso libre para proyectos personales y comerciales.  
Por favor, enlaza este repositorio cuando reutilices componentes esenciales.
