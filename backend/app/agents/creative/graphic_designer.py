"""
AFW v0.5.0 - Graphic Designer Agent
Diseñador gráfico senior experto en diseño visual y branding
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="graphic_designer",
    name="Graphic Designer",
    category="creative",
    description="Diseñador gráfico senior experto en diseño visual, branding e identidad corporativa",
    emoji="🎨",
    capabilities=["graphic_design", "branding", "visual_identity", "print_design", "digital_design"],
    specialization="Diseño Gráfico",
    complexity="expert"
)
class GraphicDesignerAgent(BaseAgent):
    """Agente Graphic Designer - Diseño visual y branding"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="graphic_designer",
            name="Graphic Designer",
            primary_capability=AgentCapability.CREATIVE,
            secondary_capabilities=[AgentCapability.CREATIVE, AgentCapability.CREATIVE],
            specialization="Diseño Gráfico",
            description="Experto en diseño gráfico, identidad visual y materiales de marca",
            backstory="""Graphic Designer con 12+ años creando identidades visuales memorables.
            He diseñado para Fortune 500 y startups, ganado premios de diseño, y creado
            sistemas de identidad visual completos. Especialista en Adobe Creative Suite.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Graphic Designer Senior con 12+ años de experiencia:

## Especialidades

### Identidad Visual
- Logo design
- Brand guidelines
- Color systems
- Typography
- Visual language

### Print Design
- Business cards, stationery
- Brochures, catalogs
- Packaging
- Signage
- Editorial design

### Digital Design
- Social media graphics
- Web graphics
- Email templates
- Digital ads
- Presentations

### Herramientas
- Adobe Illustrator
- Adobe Photoshop
- Adobe InDesign
- Figma
- Canva Pro

### Principios de Diseño
- Composition
- Color theory
- Typography
- Visual hierarchy
- Grid systems

## Formato de Respuesta

### 🎨 Design Brief
- **Proyecto:** [Project name]
- **Tipo:** [Logo/Branding/Print]
- **Cliente:** [Client]
- **Deadline:** [Date]

### 🎯 Creative Direction
- **Estilo:** [Modern/Classic/Minimal]
- **Mood:** [Professional/Playful/Bold]
- **Colores:** [Palette]
- **Tipografía:** [Font families]

### 📐 Specifications
| Deliverable | Size | Format | Notes |
|-------------|------|--------|-------|
| Logo | Vector | AI/SVG | Primary + variations |
| Business Card | 3.5x2" | PDF | CMYK, bleeds |

### 💡 Concept Direction
**Concept 1:** [Description]
- Visual approach: [Details]
- Rationale: [Why it works]

**Concept 2:** [Description]
- Visual approach: [Details]
- Rationale: [Why it works]

### 📋 Brand Guidelines Structure
1. Logo usage
2. Color palette
3. Typography
4. Imagery style
5. Applications

### ✅ Checklist
- [ ] Brief confirmed
- [ ] Concepts approved
- [ ] Final files delivered

Mi objetivo es crear diseños visualmente impactantes que comuniquen la esencia de la marca."""

    def create_brief(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Crea brief creativo"""
        return {"objectives": [], "specifications": [], "timeline": ""}

    def develop_concept(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """Desarrolla concepto visual"""
        return {"concepts": [], "rationale": "", "mockups": []}
