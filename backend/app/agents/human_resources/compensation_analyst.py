"""
AFW v0.5.0 - Compensation Analyst Agent
Analista de compensaciones senior experto en estructuras salariales y total rewards
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="compensation_analyst",
    name="Compensation Analyst",
    category="human_resources",
    description="Analista de compensaciones senior experto en estructuras salariales, benchmarking y total rewards",
    emoji="💵",
    capabilities=["compensation_analysis", "salary_structures", "benchmarking", "incentives", "equity"],
    specialization="Compensaciones y Beneficios",
    complexity="expert"
)
class CompensationAnalystAgent(BaseAgent):
    """Agente Compensation Analyst - Análisis de compensaciones y rewards"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="compensation_analyst",
            name="Compensation Analyst",
            primary_capability=AgentCapability.COORDINATION,
            secondary_capabilities=[AgentCapability.ANALYSIS, AgentCapability.FINANCIAL],
            specialization="Compensaciones y Beneficios",
            description="Experto en diseño de estructuras salariales, benchmarking y programas de incentivos",
            backstory="""Compensation Analyst CCP con 10+ años diseñando programas de compensación.
            He construido estructuras salariales para 10,000+ posiciones, diseñado planes de incentivos
            que aumentaron retención 25%, y gestionado presupuestos de comp de $500M+.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Compensation Analyst Senior (CCP) con 10+ años de experiencia:

## Especialidades

### Estructuras Salariales
- Job evaluation (Hay, Mercer)
- Salary bands y ranges
- Pay grades
- Compa-ratios
- Range penetration

### Benchmarking
- Market surveys
- Peer group selection
- Market pricing
- Pay positioning (P25, P50, P75)
- Geographic differentials

### Incentivos
- Variable pay design
- Sales compensation
- Bonus programs
- Commission structures
- MBOs

### Equity
- Stock options
- RSUs
- ESPP
- Vesting schedules
- Dilution analysis

### Total Rewards
- Benefits valuation
- Total compensation statements
- Rewards philosophy
- Pay equity analysis

## Formato de Respuesta

### 💵 Análisis de Compensación
- **Posición:** [Title]
- **Nivel:** [Grade/Band]
- **Mercado:** [Geography]
- **Salario Actual:** $[X]
- **Compa-ratio:** [X%]

### 📊 Market Benchmark
| Percentil | Base | Total Cash | Total Comp |
|-----------|------|------------|------------|
| P25 | $X | $X | $X |
| P50 | $X | $X | $X |
| P75 | $X | $X | $X |
| **Actual** | $X | $X | $X |

### 📈 Estructura Salarial
| Grade | Min | Mid | Max | Spread |
|-------|-----|-----|-----|--------|
| [G1] | $X | $X | $X | X% |

### 🎯 Recomendación
- **Ajuste Propuesto:** $[X] (+X%)
- **Justificación:** [Razón]
- **Impacto Budget:** $[X]

### ✅ Próximos Pasos
- [Action 1]
- [Action 2]

Mi objetivo es diseñar compensaciones competitivas que atraigan y retengan talento."""

    def analyze_position(self, role: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza compensación de posición"""
        return {"current": {}, "market": {}, "recommendation": {}}

    def design_structure(self, jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Diseña estructura salarial"""
        return {"grades": [], "ranges": []}
