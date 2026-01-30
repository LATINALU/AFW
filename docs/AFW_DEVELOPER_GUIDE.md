# 👨‍💻 AFW v0.5.0 - Guía del Desarrollador

> **Agents For Works** - Guía Completa para Contribuir y Escalar el Proyecto

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- Git
- Docker (opcional)

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/LATINALU/AFW.git
cd AFW

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend
cd ../frontend
npm install

# 4. Variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

### Ejecutar en Desarrollo

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🤖 Crear un Nuevo Agente

### Paso 1: Crear el Archivo

```python
# backend/app/agents/categories/[categoria]/mi_agente.py

"""
AFW v0.5.0 - Mi Agente Personalizado
Descripción breve del agente
"""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="mi_agente_id",           # ID único (snake_case)
    name="Mi Agente",                   # Nombre legible
    category="categoria",               # Una de las 10 categorías
    description="Descripción completa del agente",
    emoji="🎯",                         # Emoji representativo
    capabilities=["cap1", "cap2"],      # Lista de capacidades
    specialization="Mi Especialidad",
    complexity="basic|intermediate|advanced"
)
class MiAgenteAgent(BaseAgent):
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="mi_agente_id",
            name="Mi Agente",
            primary_capability=AgentCapability.ANALYSIS,  # Capacidad principal
            secondary_capabilities=[AgentCapability.RESEARCH],
            specialization="Mi Especialidad",
            description="Descripción detallada",
            backstory="""Historia y experiencia del agente que define su personalidad
            y expertise. Esto influye en cómo responde.""",
            model=model, 
            api_config=api_config, 
            language=language
        )
    
    def get_system_prompt(self) -> str:
        return """Eres un [rol] experto en:

## Especialidades:
- **Área 1:** Descripción
- **Área 2:** Descripción

## Metodología:
1. Paso 1
2. Paso 2
3. Paso 3

## Formato de Respuesta:
[Indicaciones de cómo estructurar respuestas]

Siempre proporciona [tipo de output esperado]."""
```

### Paso 2: Registrar en __init__.py

```python
# backend/app/agents/categories/[categoria]/__init__.py

from .mi_agente import MiAgenteAgent

CATEGORIA_AGENTS = [
    # ... agentes existentes ...
    MiAgenteAgent,  # Agregar aquí
]

__all__ = [
    # ... exports existentes ...
    "MiAgenteAgent",
]
```

### Paso 3: Verificar Registro

```python
# Test rápido
from app.agents.agent_registry import agent_registry

# Verificar que el agente está registrado
agent = agent_registry.get("mi_agente_id")
print(agent.name)  # "Mi Agente"
```

---

## 📋 Crear un Nuevo Workflow

### Estructura de Workflow

```python
# backend/app/workflows/workflow_registry.py

from app.workflows.base_workflow import (
    WorkflowTemplate, 
    WorkflowStep, 
    WorkflowComplexity
)

# Registrar nuevo workflow
workflow_registry.register(WorkflowTemplate(
    workflow_id="mi_workflow",              # ID único
    name="Mi Workflow Personalizado",
    description="Qué hace este workflow",
    category="software_development",        # Categoría
    complexity=WorkflowComplexity.MEDIUM,   # BASIC, MEDIUM, COMPLEX
    estimated_time_minutes=30,
    required_agents=["agent1", "agent2"],   # IDs de agentes necesarios
    tags=["tag1", "tag2"],
    inputs=["input1", "input2"],            # Datos de entrada
    outputs=["output1", "output2"],         # Resultados esperados
    steps=[
        WorkflowStep(
            step_id="s1",
            name="Paso 1",
            description="Descripción del paso",
            agent_id="agent1",
            prompt_template="Realiza {input1} para {input2}",
            order=1,
            dependencies=[]  # Sin dependencias = ejecutar primero
        ),
        WorkflowStep(
            step_id="s2",
            name="Paso 2", 
            description="Segundo paso",
            agent_id="agent2",
            prompt_template="Basándote en {s1_result}, haz...",
            order=2,
            dependencies=["s1"]  # Depende del paso 1
        )
    ]
))
```

---

## 🎨 Frontend: Agregar Componentes

### Usar EldoraUI

```bash
# Instalar dependencias (si no están)
npm install framer-motion clsx tailwind-merge
```

### Estructura de Componentes

```tsx
// frontend/src/components/ui/MiComponente.tsx

import React from 'react';
import { cn } from '@/lib/utils';

interface MiComponenteProps {
  title: string;
  variant?: 'default' | 'primary' | 'secondary';
  className?: string;
}

export const MiComponente: React.FC<MiComponenteProps> = ({
  title,
  variant = 'default',
  className
}) => {
  return (
    <div className={cn(
      "rounded-lg p-4 transition-all",
      variant === 'primary' && "bg-primary text-white",
      variant === 'secondary' && "bg-secondary",
      className
    )}>
      <h3>{title}</h3>
    </div>
  );
};
```

---

## 🔧 Configuración

### Variables de Entorno

```bash
# .env

# API Keys (requeridas)
GROQ_API_KEY=gsk_xxxx
OPENAI_API_KEY=sk-xxxx

# Base de datos
DATABASE_URL=sqlite:///./afw.db

# Seguridad
SECRET_KEY=tu-clave-secreta-muy-larga
JWT_ALGORITHM=HS256

# Servidor
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development  # development | staging | production

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Configuración de Agentes

```python
# backend/app/afw_config.py

# Límites
MAX_AGENTS_PER_TASK = 10      # Modificar si necesitas más
TOTAL_AGENTS = 102            # Actualizar al agregar agentes

# Modelos por defecto
DEFAULT_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

# Timeouts
AGENT_TIMEOUT_SECONDS = 60
WORKFLOW_TIMEOUT_SECONDS = 300
```

---

## 🧪 Testing

### Tests de Agentes

```python
# tests/test_agents.py

import pytest
from app.agents.agent_registry import agent_registry

def test_agent_registration():
    """Verificar que todos los agentes están registrados"""
    stats = agent_registry.get_statistics()
    assert stats["total_agents"] >= 102
    
def test_mercadolibre_agents():
    """Test específico para agentes de Mercado Libre"""
    ml_product = agent_registry.get("mercadolibre_product_specialist")
    ml_sales = agent_registry.get("mercadolibre_sales_optimizer")
    
    assert ml_product is not None
    assert ml_sales is not None
    assert ml_product.category == "marketing"

def test_agent_response():
    """Test de respuesta de agente"""
    from app.agents.categories.marketing import MercadoLibreProductSpecialistAgent
    
    agent = MercadoLibreProductSpecialistAgent()
    prompt = agent.get_system_prompt()
    
    assert "Mercado Libre" in prompt
    assert "ficha técnica" in prompt.lower()
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_agents.py -v

# Con coverage
pytest --cov=app tests/
```

---

## 📦 Deployment

### Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f backend
```

### Producción

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Configurar variables de producción
export ENVIRONMENT=production
export DATABASE_URL=postgresql://...

# 3. Ejecutar con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔄 Git Workflow

### Branches

```
main          → Producción estable
develop       → Desarrollo activo
feature/*     → Nuevas funcionalidades
fix/*         → Corrección de bugs
release/*     → Preparación de releases
```

### Commits

```bash
# Formato
<tipo>(<alcance>): <descripción>

# Ejemplos
feat(agents): add Mercado Libre specialists
fix(frontend): resolve chat scroll issue
docs(readme): update installation guide
refactor(workflow): optimize step execution
```

---

## 📊 Métricas de Calidad

### Código Python
- PEP 8 compliance
- Type hints en funciones públicas
- Docstrings en clases y métodos

### Código TypeScript
- ESLint sin errores
- Types explícitos
- Componentes con Props interface

---

## 🆘 Solución de Problemas

### Error: Agente no encontrado
```python
# Verificar registro
from app.agents.agent_registry import agent_registry
print(agent_registry.list_all())
```

### Error: Import circular
```python
# Usar imports tardíos
def get_agent():
    from app.agents.categories.marketing import MiAgente
    return MiAgente()
```

### Error: CORS en desarrollo
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/mi-feature`
3. Commits descriptivos
4. Push: `git push origin feature/mi-feature`
5. Pull Request con descripción detallada

### Checklist PR
- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] Sin errores de lint
- [ ] Revisado por al menos 1 persona

---

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [EldoraUI](https://www.eldoraui.site/)
- [Tailwind CSS](https://tailwindcss.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## 🎯 Próximos Pasos para Nuevos Desarrolladores

1. ✅ Leer esta guía completa
2. ✅ Configurar entorno local
3. ✅ Ejecutar tests existentes
4. ✅ Crear un agente de prueba
5. ✅ Hacer tu primer PR

---

*AFW v0.5.0 - Desarrollado para ayudar a la humanidad* 🌍
