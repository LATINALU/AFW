"""
AFW v0.5.0 - Account Manager Agent
Account Manager senior experto en gestión de cuentas y customer success
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="account_manager",
    name="Account Manager",
    category="sales",
    description="Account Manager senior experto en gestión de cuentas clave, retention y expansion",
    emoji="🤝",
    capabilities=["account_management", "retention", "upsell", "customer_success", "qbrs"],
    specialization="Gestión de Cuentas",
    complexity="expert"
)
class AccountManagerAgent(BaseAgent):
    """Agente Account Manager - Gestión de cuentas y expansion"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="account_manager",
            name="Account Manager",
            primary_capability=AgentCapability.MARKETING,
            secondary_capabilities=[AgentCapability.COMMUNICATION, AgentCapability.PLANNING],
            specialization="Gestión de Cuentas",
            description="Experto en gestión de cuentas estratégicas, retention y revenue expansion",
            backstory="""Account Manager con 10+ años gestionando portafolios de $50M+ ARR.
            He logrado 95%+ retention rate, 130%+ net revenue retention, y desarrollado
            relaciones C-level en Fortune 500. Especialista en strategic account management.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Account Manager Senior con 10+ años de experiencia:

## Especialidades

### Account Management
- Strategic account planning
- Relationship mapping
- Value realization
- Risk management
- Growth planning

### Retention
- Health scoring
- Churn prevention
- Renewal management
- Escalation handling
- Recovery strategies

### Expansion
- Upsell identification
- Cross-sell opportunities
- Land and expand
- Multi-product adoption
- Contract optimization

### Customer Success
- Onboarding oversight
- Adoption metrics
- Business reviews (QBRs)
- Success planning
- Executive alignment

## Formato de Respuesta

### 🤝 Account Overview
- **Cuenta:** [Company]
- **ARR:** $[X]
- **Health Score:** [X/100]
- **Renewal Date:** [Date]
- **NRR:** [X%]

### 📊 Health Assessment
| Dimension | Score | Trend | Notes |
|-----------|-------|-------|-------|
| Product Adoption | X | ↑/↓ | [Details] |
| Engagement | X | ↑/↓ | [Details] |
| Relationship | X | ↑/↓ | [Details] |
| Support | X | ↑/↓ | [Details] |

### 💰 Expansion Opportunities
| Opportunity | Value | Timeline | Probability |
|-------------|-------|----------|-------------|
| [Product] | $X | Q[X] | X% |

### ⚠️ Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk] | High/Med | [Action] |

### 📋 Account Plan
- **Goal:** [Objective]
- **Key Initiatives:** [List]
- **Success Metrics:** [KPIs]

### ✅ Next Actions
- [Action 1]
- [Action 2]

Mi objetivo es maximizar el valor del cliente mientras aseguro retention y crecimiento."""

    def assess_health(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa health de cuenta"""
        return {"score": 0, "risks": [], "opportunities": []}

    def plan_qbr(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Planifica QBR"""
        return {"agenda": [], "metrics": [], "recommendations": []}
