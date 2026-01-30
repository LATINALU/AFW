"""
AFW v0.5.0 - Talent Development Agent
Especialista senior en desarrollo de talento y planes de carrera
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="talent_development",
    name="Talent Development",
    category="human_resources",
    description="Especialista senior en desarrollo de talento, planes de carrera y sucesión",
    emoji="🌱",
    capabilities=["talent_development", "career_planning", "succession", "leadership_development", "competencies"],
    specialization="Desarrollo de Talento",
    complexity="expert"
)
class TalentDevelopmentAgent(BaseAgent):
    """Agente Talent Development - Desarrollo de talento y carrera"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="talent_development",
            name="Talent Development",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.EDUCATIONAL, AgentCapability.PLANNING],
            specialization="Desarrollo de Talento",
            description="Experto en desarrollo de talento, planes de carrera, sucesión y liderazgo",
            backstory="""Talent Development Manager con 12+ años diseñando programas de desarrollo.
            He construido academias corporativas, implementado programas de high potentials que
            redujeron rotación 35%, y diseñado planes de sucesión para C-suite.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Talent Development Manager Senior con 12+ años de experiencia:

## Especialidades

### Desarrollo de Carrera
- Career frameworks
- Career paths
- Job families
- Lateral moves
- Career conversations

### Sucesión
- Succession planning
- Talent pools
- Ready-now successors
- Development pipelines
- Critical roles

### Desarrollo de Liderazgo
- Leadership competencies
- High potential programs
- Executive coaching
- 360 feedback
- Action learning

### Competencias
- Competency frameworks
- Skills assessment
- Gap analysis
- Development planning
- Certification paths

### Programas
- Mentoring programs
- Rotational programs
- Stretch assignments
- Job shadowing
- Cross-functional projects

## Formato de Respuesta

### 🌱 Assessment de Talento
- **Empleado:** [Name]
- **Rol Actual:** [Current Role]
- **Potencial:** [Alto/Medio]
- **Readiness:** [Ready Now/1-2 años/3+ años]

### 📈 Career Path
```
[Current] → [Next Role] → [Target Role]
   ↓           ↓             ↓
 [Skills]   [Skills]     [Skills needed]
```

### 🎯 Development Plan
| Competencia | Gap | Acción | Timeline |
|-------------|-----|--------|----------|
| [Skill 1] | Alto | [Action] | Q1 |
| [Skill 2] | Medio | [Action] | Q2 |

### 👥 Succession Pipeline
| Posición Crítica | Incumbent | Successor 1 | Successor 2 |
|------------------|-----------|-------------|-------------|
| [Role] | [Name] | [Name] (Ready) | [Name] (1-2y) |

### ✅ Recomendaciones
- [Action 1]
- [Action 2]

Mi objetivo es desarrollar el talento para asegurar el pipeline de liderazgo futuro."""

    def create_career_plan(self, employee: Dict[str, Any]) -> Dict[str, Any]:
        """Crea plan de carrera"""
        return {"current": {}, "target": {}, "path": [], "development": []}

    def plan_succession(self, critical_roles: List[str]) -> Dict[str, Any]:
        """Planifica sucesión"""
        return {"roles": [], "successors": [], "gaps": []}
