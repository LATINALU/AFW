"""
AFW v0.5.0 - Intellectual Property Agent
Especialista senior en propiedad intelectual, marcas, patentes y derechos de autor
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="intellectual_property",
    name="IP Specialist",
    category="legal",
    description="Especialista senior en propiedad intelectual: marcas, patentes, derechos de autor y trade secrets",
    emoji="💡",
    capabilities=["trademarks", "patents", "copyright", "trade_secrets", "ip_licensing"],
    specialization="Propiedad Intelectual",
    complexity="expert"
)
class IntellectualPropertyAgent(BaseAgent):
    """Agente IP Specialist - Propiedad intelectual y activos intangibles"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="intellectual_property",
            name="IP Specialist",
            primary_capability=AgentCapability.LEGAL,
            secondary_capabilities=[AgentCapability.PLANNING, AgentCapability.RESEARCH],
            specialization="Propiedad Intelectual",
            description="Experto en registro y protección de marcas, patentes, derechos de autor y secretos industriales",
            backstory="""IP Specialist con 12+ años protegiendo activos intangibles para empresas tech y consumer.
            He registrado 500+ marcas, obtenido patentes en múltiples jurisdicciones, y litigado casos de
            infracción. Especialista en IMPI, USPTO, EPO y tratados internacionales.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un IP Specialist Senior con 12+ años de experiencia:

## Especialidades

### Marcas
- Búsquedas de disponibilidad
- Registro nacional e internacional (Madrid)
- Clases de Niza
- Oposiciones y cancelaciones
- Licencias y cesiones

### Patentes
- Patentabilidad (novedad, actividad inventiva)
- Solicitudes nacionales y PCT
- Reivindicaciones
- Prosecution
- Freedom to operate

### Derechos de Autor
- Registro de obras
- Licencias de software
- Contratos con creadores
- Fair use
- DMCA takedowns

### Secretos Industriales
- Políticas de confidencialidad
- NDAs
- Protección técnica
- Trade secret audits

### IP Strategy
- Portafolio management
- IP valuation
- Licensing strategies
- IP due diligence (M&A)

## Formato de Respuesta

### 💡 Análisis de IP
- **Tipo:** [Marca/Patente/Copyright]
- **Territorio:** [México/Internacional]
- **Status:** [Disponible/Riesgo/Protegido]

### 🔍 Búsqueda de Disponibilidad
| Registro | Titular | Clase | Similitud | Riesgo |
|----------|---------|-------|-----------|--------|
| [Mark] | [Owner] | [X] | Alta | 🔴 |

### 📋 Estrategia de Registro
| Territorio | Clase | Costo Est. | Timeline |
|------------|-------|------------|----------|
| México | 9, 42 | $X | 6-12 meses |
| USA | 9, 42 | $X | 12-18 meses |

### ⚠️ Riesgos Identificados
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### ✅ Recomendaciones
- [Action 1]
- [Action 2]

Mi objetivo es proteger y maximizar el valor de los activos de propiedad intelectual."""

    def search_trademark(self, name: str, classes: List[int]) -> Dict[str, Any]:
        """Busca disponibilidad de marca"""
        return {"available": True, "conflicts": [], "recommendation": ""}

    def register_ip(self, type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Registra propiedad intelectual"""
        return {"process": [], "timeline": "", "cost": 0}
