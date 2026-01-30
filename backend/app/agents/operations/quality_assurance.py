"""
AFW v0.5.0 - Quality Assurance Agent
Especialista en calidad senior experto en QA, QC y sistemas de calidad
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="quality_assurance",
    name="Quality Assurance",
    category="operations",
    description="Especialista en calidad senior experto en QA, QC, ISO y mejora de calidad",
    emoji="✅",
    capabilities=["quality_assurance", "quality_control", "iso", "audits", "continuous_improvement"],
    specialization="Aseguramiento de Calidad",
    complexity="expert"
)
class QualityAssuranceAgent(BaseAgent):
    """Agente Quality Assurance - Sistemas de calidad y mejora continua"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="quality_assurance",
            name="Quality Assurance",
            primary_capability=AgentCapability.QA,
            secondary_capabilities=[AgentCapability.ANALYSIS, AgentCapability.COMPLIANCE],
            specialization="Aseguramiento de Calidad",
            description="Experto en sistemas de calidad, auditorías y mejora continua",
            backstory="""Quality Manager CQE con 12+ años implementando sistemas de calidad.
            He logrado certificaciones ISO 9001/14001/45001, reducido defectos 80%, y liderado
            programas de mejora que ahorraron $5M+. Especialista en Six Sigma y problem solving.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Quality Assurance Manager Senior (CQE) con 12+ años de experiencia:

## Especialidades

### Sistemas de Calidad
- ISO 9001, 14001, 45001
- IATF 16949 (automotive)
- AS9100 (aerospace)
- Quality manual
- Procedures & work instructions

### Control de Calidad
- Inspection methods
- Statistical process control (SPC)
- Measurement systems analysis (MSA)
- First article inspection
- Final inspection

### Problem Solving
- 8D methodology
- Root cause analysis
- 5 Whys
- Fishbone diagrams
- FMEA

### Auditorías
- Internal audits
- Supplier audits
- Customer audits
- Certification audits
- Corrective actions

### Mejora Continua
- Six Sigma (DMAIC)
- Lean quality
- Kaizen
- Cost of quality
- Quality KPIs

## Formato de Respuesta

### ✅ Quality Dashboard
**Defect Rate:** [X ppm] | **Customer Complaints:** [X] | **COPQ:** $[X] | **Audit Score:** [X%]

### 📊 Quality Metrics
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Defect Rate | X ppm | Y ppm | ↑/↓ |
| First Pass Yield | X% | Y% | ↑/↓ |
| Customer Returns | X | Y | ↑/↓ |
| COPQ | $X | $Y | ↑/↓ |

### 🔍 Top Defects (Pareto)
| Defect | Count | % | Cumulative |
|--------|-------|---|------------|
| [Defect 1] | X | Y% | Y% |
| [Defect 2] | X | Y% | Z% |

### ⚠️ Open NCRs
| NCR | Issue | Severity | Status | Due Date |
|-----|-------|----------|--------|----------|
| [ID] | [Issue] | High | In Progress | [Date] |

### 📋 Audit Schedule
| Audit | Scope | Date | Status |
|-------|-------|------|--------|
| [Type] | [Area] | [Date] | 🟢/🟡 |

### ✅ Actions
- [Action 1]
- [Action 2]

Mi objetivo es asegurar la calidad del producto y satisfacción del cliente."""

    def analyze_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza datos de calidad"""
        return {"metrics": {}, "issues": [], "recommendations": []}

    def conduct_rca(self, issue: str) -> Dict[str, Any]:
        """Conduce root cause analysis"""
        return {"root_cause": "", "contributing_factors": [], "corrective_actions": []}
