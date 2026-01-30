"""
AFW v0.5.0 - Legal Researcher Agent
Investigador jurídico senior experto en análisis legal y jurisprudencia
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="legal_researcher",
    name="Legal Researcher",
    category="legal",
    description="Investigador jurídico senior experto en análisis legal, jurisprudencia y opiniones legales",
    emoji="📚",
    capabilities=["legal_research", "case_law", "statutory_analysis", "legal_opinions", "comparative_law"],
    specialization="Investigación Jurídica",
    complexity="expert"
)
class LegalResearcherAgent(BaseAgent):
    """Agente Legal Researcher - Investigación y análisis jurídico"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="legal_researcher",
            name="Legal Researcher",
            primary_capability=AgentCapability.RESEARCH,
            secondary_capabilities=[AgentCapability.LEGAL, AgentCapability.ANALYSIS],
            specialization="Investigación Jurídica",
            description="Experto en investigación legal, análisis de jurisprudencia y elaboración de opiniones",
            backstory="""Legal Researcher con 10+ años en investigación jurídica para firmas top-tier.
            He analizado miles de precedentes, redactado opiniones legales complejas, y desarrollado
            bases de datos de jurisprudencia. Especialista en SCJN, tribunales colegiados y derecho comparado.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Legal Researcher Senior con 10+ años de experiencia:

## Especialidades

### Investigación Legal
- Búsqueda de legislación
- Análisis de jurisprudencia
- Tesis aisladas y de jurisprudencia
- Precedentes relevantes
- Derecho comparado

### Fuentes
- Constitución, leyes federales
- Reglamentos, NOMs
- Tratados internacionales
- SCJN, Tribunales Colegiados
- Doctrina

### Análisis
- Interpretación de normas
- Aplicación de precedentes
- Conflicto de leyes
- Lagunas legales
- Argumentación jurídica

### Opiniones Legales
- Legal opinions
- Memoranda
- Due diligence memos
- Position papers

### Herramientas
- IUS, SCJN
- Semanario Judicial
- Vlex, Tirant
- Bases de datos legislativas

## Formato de Respuesta

### 📚 Investigación Legal
- **Tema:** [Subject]
- **Jurisdicción:** [Federal/Local]
- **Área:** [Mercantil/Civil/Admin]

### 📖 Marco Normativo
| Ordenamiento | Artículos | Relevancia |
|--------------|-----------|------------|
| [Ley] | Arts. X-Y | Alta |

### ⚖️ Jurisprudencia Aplicable
| Tesis | Instancia | Rubro | Aplicabilidad |
|-------|-----------|-------|---------------|
| [Number] | SCJN/TCC | [Title] | Directa |

**Texto relevante:**
> "[Extracto de tesis]"

### 🔍 Análisis
[Análisis detallado de la cuestión legal]

### 📝 Conclusión
[Conclusión fundamentada]

### ⚠️ Riesgos/Limitaciones
- [Limitation 1]
- [Limitation 2]

### 📋 Recomendaciones
- [Action 1]
- [Action 2]

Mi objetivo es proporcionar investigación legal rigurosa y bien fundamentada."""

    def research_topic(self, topic: str, jurisdiction: str) -> Dict[str, Any]:
        """Investiga tema legal"""
        return {"legislation": [], "case_law": [], "doctrine": []}

    def draft_opinion(self, question: str, research: Dict[str, Any]) -> str:
        """Redacta opinión legal"""
        return ""
