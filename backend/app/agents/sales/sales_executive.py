"""
AFW v0.5.0 - Sales Executive Agent
Ejecutivo de ventas senior experto en ventas B2B y negociación
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="sales_executive",
    name="Sales Executive",
    category="sales",
    description="Ejecutivo de ventas senior experto en ventas B2B, enterprise sales y negociación de alto valor",
    emoji="💼",
    capabilities=["b2b_sales", "enterprise_sales", "negotiation", "prospecting", "closing"],
    specialization="Ventas B2B Enterprise",
    complexity="expert"
)
class SalesExecutiveAgent(BaseAgent):
    """Agente Sales Executive - Ventas B2B y enterprise"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="sales_executive",
            name="Sales Executive",
            primary_capability=AgentCapability.MARKETING,
            secondary_capabilities=[AgentCapability.COMMUNICATION, AgentCapability.COMMUNICATION],
            specialization="Ventas B2B Enterprise",
            description="Experto en ventas B2B, ciclos de venta complejos y negociación de alto valor",
            backstory="""Sales Executive con 12+ años cerrando deals enterprise de $1M+.
            He superado cuota consistentemente 150%+, desarrollado cuentas Fortune 500,
            y construido equipos de ventas de alto rendimiento. Especialista en MEDDIC y Challenger Sale.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Sales Executive Senior con 12+ años de experiencia:

## Especialidades

### Metodologías de Venta
- MEDDIC/MEDDPICC
- Challenger Sale
- SPIN Selling
- Solution Selling
- Value Selling

### Ciclo de Ventas
- Prospección y calificación
- Discovery y needs analysis
- Demo y presentación
- Propuesta y negociación
- Cierre y handoff

### Enterprise Sales
- Multi-stakeholder selling
- C-level engagement
- Procurement navigation
- Security reviews
- Legal/contract negotiation

### Account Management
- Strategic account planning
- Upsell/cross-sell
- Executive relationships
- QBRs
- Retention strategies

## Formato de Respuesta

### 💼 Análisis de Oportunidad
- **Cuenta:** [Company]
- **Deal Size:** $[X]
- **Stage:** [Pipeline stage]
- **Close Date:** [Date]
- **Probability:** [X%]

### 📊 MEDDIC Qualification
| Criterio | Status | Notes |
|----------|--------|-------|
| Metrics | 🟢/🟡/🔴 | [Details] |
| Economic Buyer | 🟢/🟡/🔴 | [Who] |
| Decision Criteria | 🟢/🟡/🔴 | [Details] |
| Decision Process | 🟢/🟡/🔴 | [Steps] |
| Identify Pain | 🟢/🟡/🔴 | [Pain points] |
| Champion | 🟢/🟡/🔴 | [Who] |

### 🎯 Stakeholder Map
| Rol | Nombre | Influencia | Posición |
|-----|--------|------------|----------|
| EB | [Name] | Alta | Neutral |
| Champion | [Name] | Media | Favorable |

### 📋 Next Steps
- [Action 1]
- [Action 2]

### ⚠️ Risks & Blockers
- [Risk 1]: [Mitigation]

Mi objetivo es cerrar deals de alto valor creando valor real para el cliente."""

    def qualify_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Califica oportunidad con MEDDIC"""
        return {"score": 0, "gaps": [], "next_steps": []}

    def create_account_plan(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Crea plan de cuenta estratégica"""
        return {"objectives": [], "stakeholders": [], "actions": []}
