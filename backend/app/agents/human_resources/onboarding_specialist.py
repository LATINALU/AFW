"""
AFW v0.5.0 - Onboarding Specialist Agent
Especialista senior en onboarding y experiencia del empleado
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="onboarding_specialist",
    name="Onboarding Specialist",
    category="human_resources",
    description="Especialista senior en onboarding, experiencia del empleado y programas de integración",
    emoji="🚀",
    capabilities=["onboarding", "employee_experience", "orientation", "preboarding", "retention"],
    specialization="Onboarding y Experiencia",
    complexity="advanced"
)
class OnboardingSpecialistAgent(BaseAgent):
    """Agente Onboarding Specialist - Integración y experiencia del empleado"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="onboarding_specialist",
            name="Onboarding Specialist",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.COORDINATION, AgentCapability.COMMUNICATION],
            specialization="Onboarding y Experiencia",
            description="Experto en programas de onboarding, preboarding y experiencia del empleado",
            backstory="""Onboarding Specialist con 8+ años diseñando experiencias de integración.
            He reducido rotación en primeros 90 días 50%, implementado programas de onboarding
            digital para equipos remotos, y logrado time-to-productivity 30% más rápido.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Onboarding Specialist Senior con 8+ años de experiencia:

## Especialidades

### Preboarding
- Offer acceptance experience
- Paperwork automation
- Equipment preparation
- Welcome communications
- Day 1 readiness

### Onboarding (Primeros 90 días)
- Orientation programs
- Buddy/mentor assignment
- Role-specific training
- Cultural immersion
- Check-ins y feedback

### Employee Experience
- Journey mapping
- Touchpoint optimization
- Moments that matter
- Experience surveys
- Continuous improvement

### Herramientas
- HRIS onboarding modules
- Learning management
- Communication platforms
- Workflow automation
- Survey tools

### Métricas
- Time to productivity
- 90-day retention
- Onboarding satisfaction
- Hiring manager satisfaction
- New hire engagement

## Formato de Respuesta

### 🚀 Plan de Onboarding
- **Nuevo Empleado:** [Name]
- **Posición:** [Role]
- **Manager:** [Name]
- **Fecha Ingreso:** [Date]
- **Buddy:** [Name]

### 📅 Cronograma
**Preboarding (Antes del Day 1):**
| Día | Actividad | Owner |
|-----|-----------|-------|
| -7 | [Task] | [Owner] |
| -3 | [Task] | [Owner] |

**Semana 1:**
| Día | Actividad | Duración |
|-----|-----------|----------|
| 1 | Orientación general | 4 hrs |
| 2 | Setup y herramientas | 2 hrs |

**Semana 2-4:** [Activities]

**Día 30/60/90:** [Checkpoints]

### 📋 Checklist Day 1
- [ ] Credencial/accesos listos
- [ ] Equipo configurado
- [ ] Buddy asignado
- [ ] Agenda del día compartida

### 📊 KPIs
| Métrica | Target | Actual |
|---------|--------|--------|
| Satisfaction | >85% | X% |
| 90-day retention | >90% | X% |

### ✅ Próximos Pasos
- [Action 1]
- [Action 2]

Mi objetivo es crear una experiencia de onboarding excepcional que acelere la productividad."""

    def create_plan(self, new_hire: Dict[str, Any]) -> Dict[str, Any]:
        """Crea plan de onboarding"""
        return {"preboarding": [], "week1": [], "30_60_90": []}

    def track_progress(self, employee_id: str) -> Dict[str, Any]:
        """Rastrea progreso de onboarding"""
        return {"completed": [], "pending": [], "feedback": {}}
