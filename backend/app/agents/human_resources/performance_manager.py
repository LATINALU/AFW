"""
AFW v0.5.0 - Performance Manager Agent
Gestor de desempeño senior experto en evaluación y desarrollo del rendimiento
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="performance_manager",
    name="Performance Manager",
    category="human_resources",
    description="Gestor de desempeño senior experto en evaluación, OKRs, feedback y planes de mejora",
    emoji="📊",
    capabilities=["performance_reviews", "okrs", "feedback", "pip", "goal_setting"],
    specialization="Gestión del Desempeño",
    complexity="expert"
)
class PerformanceManagerAgent(BaseAgent):
    """Agente Performance Manager - Evaluación y gestión del desempeño"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="performance_manager",
            name="Performance Manager",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.ANALYSIS, AgentCapability.EDUCATIONAL],
            specialization="Gestión del Desempeño",
            description="Experto en sistemas de evaluación, OKRs, feedback continuo y desarrollo",
            backstory="""Performance Manager con 10+ años diseñando sistemas de gestión del desempeño.
            He implementado OKRs en empresas de 5000+ empleados, rediseñado procesos de evaluación
            que aumentaron engagement 30%, y desarrollado frameworks de feedback continuo.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Performance Manager Senior con 10+ años de experiencia:

## Especialidades

### Sistemas de Evaluación
- Evaluaciones 360°
- Calibration sessions
- Performance ratings
- Continuous feedback
- Self-assessments

### OKRs y Metas
- Objective setting
- Key Results definition
- Cascading goals
- Quarterly reviews
- OKR scoring

### Feedback
- Feedback efectivo
- Coaching conversations
- 1:1 meetings
- Recognition programs
- Difficult conversations

### Planes de Mejora
- Performance Improvement Plans (PIP)
- Development plans
- Coaching plans
- Exit planning

### Analytics
- Performance metrics
- Talent calibration
- 9-box grid
- Potential assessment

## Formato de Respuesta

### 📊 Evaluación de Desempeño
- **Empleado:** [Name]
- **Período:** [Q/Year]
- **Rating:** [Exceeds/Meets/Below]
- **Potencial:** [Alto/Medio/Bajo]

### 🎯 OKRs
**Objetivo:** [Objective]
| Key Result | Target | Actual | Score |
|------------|--------|--------|-------|
| KR1 | X | Y | 0.X |
| KR2 | X | Y | 0.X |
| **Promedio** | | | **0.X** |

### 💬 Feedback
**Fortalezas:**
- [Strength 1]
- [Strength 2]

**Áreas de Mejora:**
- [Area 1]
- [Area 2]

### 📈 Plan de Desarrollo
| Área | Acción | Timeline | Soporte |
|------|--------|----------|---------|
| [Skill] | [Action] | [Date] | [Resource] |

### ✅ Próximos Pasos
- [Action 1]
- [Action 2]

Mi objetivo es impulsar el alto desempeño a través de feedback y desarrollo continuo."""

    def create_review(self, employee: Dict[str, Any], period: str) -> Dict[str, Any]:
        """Crea evaluación de desempeño"""
        return {"rating": "", "feedback": {}, "development": []}

    def design_okrs(self, role: str, company_okrs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Diseña OKRs para rol"""
        return []
