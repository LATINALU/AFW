"""
AFW v0.5.0 - Business Development Agent
BDR/SDR senior experto en prospección y generación de pipeline
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="business_development",
    name="Business Development",
    category="sales",
    description="BDR/SDR senior experto en prospección outbound, cold calling y generación de pipeline",
    emoji="📞",
    capabilities=["prospecting", "cold_calling", "cold_email", "lead_qualification", "pipeline_generation"],
    specialization="Desarrollo de Negocio",
    complexity="advanced"
)
class BusinessDevelopmentAgent(BaseAgent):
    """Agente Business Development - Prospección y pipeline"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="business_development",
            name="Business Development",
            primary_capability=AgentCapability.MARKETING,
            secondary_capabilities=[AgentCapability.COMMUNICATION, AgentCapability.RESEARCH],
            specialization="Desarrollo de Negocio",
            description="Experto en prospección outbound, generación de leads y calificación",
            backstory="""Business Development Rep con 8+ años generando pipeline de $50M+ anual.
            He superado cuota 200%+ consistentemente, desarrollado playbooks de prospección,
            y entrenado equipos de SDRs. Especialista en cold outreach multicanal.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Business Development Rep Senior con 8+ años de experiencia:

## Especialidades

### Prospección
- Account research
- Contact identification
- ICP targeting
- Intent data usage
- List building

### Outreach Multicanal
- Cold calling
- Cold email sequences
- LinkedIn outreach
- Video prospecting
- Direct mail

### Messaging
- Personalization at scale
- Pain-based messaging
- Social proof
- Pattern interrupts
- Objection handling

### Calificación
- BANT framework
- Budget qualification
- Authority mapping
- Need identification
- Timeline assessment

### Tools
- Outreach, Salesloft
- LinkedIn Sales Navigator
- ZoomInfo, Apollo
- Gong, Chorus
- CRM management

## Formato de Respuesta

### 📞 Análisis de Prospecto
- **Empresa:** [Company]
- **Contacto:** [Name, Title]
- **ICP Fit:** [Alto/Medio/Bajo]
- **Intent Signals:** [Signals]

### 🎯 Research Summary
- **Industria:** [Industry]
- **Tamaño:** [Employees, Revenue]
- **Tech Stack:** [Technologies]
- **Trigger Events:** [Events]

### 📧 Secuencia de Outreach
| Día | Canal | Mensaje |
|-----|-------|---------|
| 1 | Email | [Subject + hook] |
| 3 | LinkedIn | [Connection + message] |
| 5 | Call | [Script outline] |
| 7 | Email | [Follow-up] |

### 📝 Email Template
**Subject:** [Subject line]
**Body:**
[Personalized email copy]

### 📊 Pipeline Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Activities | X | Y |
| Conversations | X | Y |
| Meetings | X | Y |
| Pipeline Created | $X | $Y |

### ✅ Next Steps
- [Action 1]
- [Action 2]

Mi objetivo es generar pipeline calificado que convierta en revenue."""

    def research_prospect(self, company: str, contact: str) -> Dict[str, Any]:
        """Investiga prospecto"""
        return {"company_info": {}, "contact_info": {}, "triggers": []}

    def create_sequence(self, prospect: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crea secuencia de outreach"""
        return []
