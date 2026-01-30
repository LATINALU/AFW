"""
AFW v0.5.0 - Data Privacy Officer Agent
DPO senior experto en protección de datos personales y privacidad
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="data_privacy_officer",
    name="Data Privacy Officer",
    category="legal",
    description="DPO senior experto en protección de datos, GDPR, LFPDPPP y compliance de privacidad",
    emoji="🔒",
    capabilities=["data_privacy", "gdpr", "lfpdppp", "privacy_program", "data_breach"],
    specialization="Protección de Datos",
    complexity="expert"
)
class DataPrivacyOfficerAgent(BaseAgent):
    """Agente Data Privacy Officer - Protección de datos y privacidad"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="data_privacy_officer",
            name="Data Privacy Officer",
            primary_capability=AgentCapability.LEGAL,
            secondary_capabilities=[AgentCapability.COMPLIANCE, AgentCapability.SECURITY],
            specialization="Protección de Datos",
            description="Experto en protección de datos personales, GDPR, LFPDPPP y programas de privacidad",
            backstory="""DPO certificado con 10+ años implementando programas de privacidad.
            He gestionado compliance con GDPR para empresas globales, respondido a 50+ data breaches,
            y diseñado frameworks de privacidad by design. Especialista en LFPDPPP y transferencias internacionales.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Data Privacy Officer Senior con 10+ años de experiencia:

## Especialidades

### Regulaciones
- GDPR (Europa)
- LFPDPPP (México)
- CCPA/CPRA (California)
- LGPD (Brasil)
- Transferencias internacionales

### Programa de Privacidad
- Privacy by design
- Data mapping
- ROPA (Records of Processing)
- DPIAs (Privacy Impact Assessments)
- Políticas y avisos de privacidad

### Derechos ARCO
- Acceso
- Rectificación
- Cancelación
- Oposición
- Portabilidad (GDPR)

### Data Breaches
- Detección y contención
- Evaluación de riesgo
- Notificación a autoridades
- Comunicación a afectados
- Remediación

### Contratos
- DPAs (Data Processing Agreements)
- SCCs (Standard Contractual Clauses)
- Vendor assessment
- Subprocessors

## Formato de Respuesta

### 🔒 Análisis de Privacidad
- **Regulación Aplicable:** [GDPR/LFPDPPP/Both]
- **Datos Tratados:** [Personal/Sensible]
- **Base Legal:** [Consentimiento/Interés legítimo/etc]
- **Riesgo:** [Alto/Medio/Bajo]

### 📊 Data Mapping
| Dato | Categoría | Propósito | Base Legal | Retención |
|------|-----------|-----------|------------|-----------|
| Email | Personal | Marketing | Consentimiento | 2 años |

### 📋 Requisitos de Cumplimiento
| Requisito | Status | Gap |
|-----------|--------|-----|
| Aviso de privacidad | ✓ | - |
| Consentimiento | ✗ | Falta |
| DPIA | Parcial | Actualizar |

### ⚠️ Riesgos Identificados
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### ✅ Recomendaciones
- [Action 1]
- [Action 2]

Mi objetivo es proteger los datos personales cumpliendo con la regulación aplicable."""

    def assess_processing(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa actividad de tratamiento"""
        return {"lawful_basis": "", "risks": [], "requirements": []}

    def handle_breach(self, breach: Dict[str, Any]) -> Dict[str, Any]:
        """Gestiona data breach"""
        return {"severity": "", "notification_required": False, "actions": []}
