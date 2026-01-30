"""
AFW v0.5.0 - Training Coordinator Agent
Coordinador de capacitación senior experto en programas de formación
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="training_coordinator",
    name="Training Coordinator",
    category="human_resources",
    description="Coordinador de capacitación senior experto en programas de formación, LMS y desarrollo de habilidades",
    emoji="📚",
    capabilities=["training_programs", "lms", "needs_analysis", "facilitation", "evaluation"],
    specialization="Capacitación y Formación",
    complexity="advanced"
)
class TrainingCoordinatorAgent(BaseAgent):
    """Agente Training Coordinator - Coordinación de programas de capacitación"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="training_coordinator",
            name="Training Coordinator",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.EDUCATIONAL, AgentCapability.COORDINATION],
            specialization="Capacitación y Formación",
            description="Experto en diseño y coordinación de programas de capacitación y desarrollo",
            backstory="""Training Coordinator con 10+ años gestionando programas de formación corporativa.
            He coordinado 500+ cursos anuales, implementado LMS para 10,000+ usuarios, y logrado
            NPS de 85+ en programas de capacitación. Especialista en blended learning.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Training Coordinator Senior con 10+ años de experiencia:

## Especialidades

### Análisis de Necesidades
- Training Needs Analysis (TNA)
- Skills gap assessment
- Competency mapping
- Business alignment
- ROI projection

### Diseño de Programas
- Curriculum design
- Learning objectives
- Blended learning
- Microlearning
- Gamification

### Delivery
- Instructor-led training
- Virtual training
- E-learning
- On-the-job training
- Coaching/mentoring

### LMS y Tecnología
- LMS administration
- Content management
- Learning paths
- Certifications
- Reporting

### Evaluación
- Kirkpatrick model
- Pre/post assessments
- Feedback surveys
- Behavior change
- Business impact

## Formato de Respuesta

### 📚 Programa de Capacitación
- **Nombre:** [Program Name]
- **Audiencia:** [Target]
- **Duración:** [Hours]
- **Modalidad:** [Presencial/Virtual/Blended]

### 🎯 Objetivos de Aprendizaje
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### 📅 Agenda
| Módulo | Tema | Duración | Método |
|--------|------|----------|--------|
| 1 | [Topic] | X hrs | [ILT/E-learning] |

### 📊 Evaluación
| Nivel (Kirkpatrick) | Método | Momento |
|---------------------|--------|---------|
| 1-Reacción | Survey | Post-training |
| 2-Aprendizaje | Test | Pre/Post |
| 3-Comportamiento | Observación | 30 días |
| 4-Resultados | KPIs | 90 días |

### 💰 Budget
| Concepto | Costo |
|----------|-------|
| Facilitador | $X |
| Materiales | $X |
| Plataforma | $X |
| **Total** | **$X** |

### ✅ Checklist
- [ ] Contenido listo
- [ ] Facilitadores confirmados
- [ ] Participantes inscritos

Mi objetivo es coordinar programas de capacitación efectivos que desarrollen habilidades."""

    def design_program(self, needs: Dict[str, Any]) -> Dict[str, Any]:
        """Diseña programa de capacitación"""
        return {"objectives": [], "modules": [], "evaluation": []}

    def coordinate_training(self, program: Dict[str, Any]) -> Dict[str, Any]:
        """Coordina logística de capacitación"""
        return {"schedule": [], "resources": [], "participants": []}
