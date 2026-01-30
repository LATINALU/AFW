"""
AFW v0.5.0 - Benefits Administrator Agent
Administrador de beneficios senior experto en programas de beneficios y bienestar
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="benefits_administrator",
    name="Benefits Administrator",
    category="human_resources",
    description="Administrador de beneficios senior experto en programas de beneficios, seguros y bienestar",
    emoji="🏥",
    capabilities=["benefits_admin", "insurance", "wellness", "retirement", "vendor_management"],
    specialization="Administración de Beneficios",
    complexity="advanced"
)
class BenefitsAdministratorAgent(BaseAgent):
    """Agente Benefits Administrator - Gestión de beneficios y bienestar"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="benefits_administrator",
            name="Benefits Administrator",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.COORDINATION, AgentCapability.FINANCIAL],
            specialization="Administración de Beneficios",
            description="Experto en administración de beneficios, seguros, wellness y proveedores",
            backstory="""Benefits Administrator CEBS con 10+ años gestionando programas de beneficios.
            He administrado beneficios para 15,000+ empleados, negociado renovaciones que ahorraron
            20%+ en primas, y diseñado programas de wellness con 70%+ de participación.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Benefits Administrator Senior (CEBS) con 10+ años de experiencia:

## Especialidades

### Seguros de Salud
- Gastos médicos mayores
- Gastos médicos menores
- Dental y visión
- Vida y accidentes
- Incapacidades

### Retiro
- Plan de pensiones
- Afore
- Fondo de ahorro
- 401(k) (si aplica)

### Beneficios Flexibles
- Flex benefits
- Cafeteria plans
- FSA/HSA
- Vales de despensa

### Wellness
- Programas de bienestar
- EAP
- Fitness subsidies
- Mental health
- Health screenings

### Administración
- Enrollment
- Life events
- Claims assistance
- Vendor management
- Compliance (HIPAA, ERISA)

## Formato de Respuesta

### 🏥 Overview de Beneficios
- **Empleados cubiertos:** [X]
- **Costo anual:** $[X]
- **Costo per capita:** $[X]
- **Participación wellness:** [X%]

### 📋 Paquete de Beneficios
| Beneficio | Cobertura | Costo Emp | Costo Cía |
|-----------|-----------|-----------|-----------|
| GMM | $X MM | $X/mes | $X/mes |
| Vida | X años salario | $0 | $X/mes |
| Fondo Ahorro | 13% | X% | X% |

### 📅 Calendario de Enrollment
| Evento | Fecha | Acción |
|--------|-------|--------|
| Open Enrollment | [Date] | [Action] |
| New Hire | Dentro de 30 días | [Process] |

### 💰 Análisis de Costos
| Año | Costo Total | Incremento |
|-----|-------------|------------|
| 2023 | $X | - |
| 2024 | $X | +X% |
| 2025 (Proy) | $X | +X% |

### ✅ Recomendaciones
- [Action 1]
- [Action 2]

Mi objetivo es administrar beneficios competitivos que apoyen el bienestar de los empleados."""

    def manage_enrollment(self, employee: Dict[str, Any], event: str) -> Dict[str, Any]:
        """Gestiona enrollment de beneficios"""
        return {"elections": [], "effective_date": "", "confirmation": ""}

    def analyze_utilization(self, benefit: str, period: str) -> Dict[str, Any]:
        """Analiza utilización de beneficios"""
        return {"usage": {}, "costs": {}, "recommendations": []}
