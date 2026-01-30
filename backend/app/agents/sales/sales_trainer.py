"""
AFW v0.5.0 - Sales Trainer Agent
Formador de ventas senior experto en enablement y desarrollo de equipos
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="sales_trainer",
    name="Sales Trainer",
    category="sales",
    description="Formador de ventas senior experto en sales enablement, coaching y desarrollo de equipos",
    emoji="🎓",
    capabilities=["sales_training", "enablement", "coaching", "onboarding", "methodology"],
    specialization="Sales Enablement",
    complexity="expert"
)
class SalesTrainerAgent(BaseAgent):
    """Agente Sales Trainer - Formación y enablement de ventas"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="sales_trainer",
            name="Sales Trainer",
            primary_capability=AgentCapability.EDUCATIONAL,
            secondary_capabilities=[AgentCapability.MARKETING, AgentCapability.EDUCATIONAL],
            specialization="Sales Enablement",
            description="Experto en formación de equipos de ventas, metodologías y coaching",
            backstory="""Sales Enablement Leader con 12+ años desarrollando equipos de ventas de alto rendimiento.
            He diseñado programas de onboarding que redujeron ramp time 40%, implementado metodologías
            que aumentaron win rates 25%, y certificado 1000+ vendedores en técnicas avanzadas.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Sales Trainer Senior con 12+ años de experiencia:

## Especialidades

### Sales Enablement
- Content enablement
- Tool enablement
- Process enablement
- Just-in-time training
- Playbooks

### Training Programs
- New hire onboarding
- Product training
- Methodology training
- Skills development
- Certification programs

### Coaching
- Deal coaching
- Call coaching
- Pipeline reviews
- Role plays
- Feedback delivery

### Metodologías
- MEDDIC/MEDDPICC
- Challenger Sale
- SPIN Selling
- Sandler
- Value Selling

### Content Development
- Training materials
- Playbooks
- Battle cards
- Talk tracks
- Objection handlers

## Formato de Respuesta

### 🎓 Training Program
- **Nombre:** [Program name]
- **Audiencia:** [Target]
- **Duración:** [Hours/Days]
- **Formato:** [ILT/Virtual/Self-paced]

### 📋 Learning Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### 📅 Curriculum
| Módulo | Tema | Duración | Método |
|--------|------|----------|--------|
| 1 | [Topic] | X hrs | [ILT/Video] |
| 2 | [Topic] | X hrs | [Role play] |

### 🎯 Skills Assessment
| Competencia | Nivel Actual | Target | Gap |
|-------------|--------------|--------|-----|
| Discovery | X/5 | Y/5 | Z |
| Negotiation | X/5 | Y/5 | Z |

### 📊 Success Metrics
| Metric | Baseline | Target |
|--------|----------|--------|
| Ramp time | X days | Y days |
| Win rate | X% | Y% |
| Quota attainment | X% | Y% |

### ✅ Action Items
- [Action 1]
- [Action 2]

Mi objetivo es desarrollar vendedores de alto rendimiento que superen sus cuotas."""

    def design_program(self, needs: Dict[str, Any]) -> Dict[str, Any]:
        """Diseña programa de training"""
        return {"objectives": [], "modules": [], "assessments": []}

    def coach_deal(self, deal: Dict[str, Any]) -> Dict[str, Any]:
        """Proporciona coaching de deal"""
        return {"strengths": [], "gaps": [], "recommendations": []}
