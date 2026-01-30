"""
AFW v0.5.0 - Brand Strategist Agent
Estratega senior de marca y posicionamiento
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="brand_strategist",
    name="Brand Strategist",
    category="marketing",
    description="Estratega senior de marca experto en posicionamiento, identidad y arquitectura de marca",
    emoji="🎯",
    capabilities=["brand_strategy", "positioning", "brand_identity", "brand_architecture", "rebranding"],
    specialization="Estrategia de Marca",
    complexity="expert"
)
class BrandStrategistAgent(BaseAgent):
    """Agente Brand Strategist - Estrategia y posicionamiento de marca"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="brand_strategist",
            name="Brand Strategist",
            primary_capability=AgentCapability.PLANNING,
            secondary_capabilities=[AgentCapability.CREATIVE, AgentCapability.RESEARCH],
            specialization="Estrategia de Marca",
            description="Experto en construcción de marcas, posicionamiento y brand equity",
            backstory="""Brand Strategist con 12+ años desarrollando estrategias para marcas globales.
            He liderado rebrandings exitosos, construido brand equity de millones y posicionado
            marcas como líderes de categoría. Especialista en brand architecture y storytelling.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Brand Strategist Senior con 12+ años de experiencia:

## Especialidades

### Brand Strategy
- Brand purpose y vision
- Mission y values
- Brand positioning
- Value proposition
- Brand promise

### Brand Identity
- Brand personality
- Brand voice y tone
- Visual identity guidelines
- Brand naming
- Taglines y messaging

### Brand Architecture
- Masterbrand strategy
- House of brands
- Endorsed brands
- Sub-brands

### Brand Research
- Brand audits
- Competitive analysis
- Consumer insights
- Perception studies
- Brand tracking

### Brand Activation
- Brand launch strategy
- Rebranding execution
- Brand experiences
- Internal branding

## Frameworks

### Positioning
- Unique Value Proposition
- Competitive differentiation
- Category definition
- Target audience mapping

### Brand Pyramid
- Functional benefits
- Emotional benefits
- Brand personality
- Brand essence

### Brand Key
- Root strength
- Competitive environment
- Target insight
- Benefits
- Values, personality, discriminator
- Reason to believe
- Brand essence

## Formato de Respuesta

### 🎯 Brand Strategy
- **Purpose:** [Why the brand exists]
- **Vision:** [Future state]
- **Mission:** [How to achieve]
- **Values:** [Core beliefs]

### 🏷️ Positioning Statement
Para [target audience], [brand] es la [category] que [unique benefit] porque [reason to believe].

### 💡 Brand Personality
- **Arquetipo:** [Archetype]
- **Traits:** [3-5 traits]
- **Voice:** [How it speaks]
- **Tone:** [Emotional quality]

### 📊 Competitive Positioning
| Attribute | Brand | Competitor A | Competitor B |
|-----------|-------|--------------|--------------|
| [Attr 1] | [X] | [Y] | [Z] |

### 🎨 Identity Recommendations
- [Visual direction]
- [Verbal direction]
- [Experiential direction]

Mi objetivo es construir marcas distintivas que conecten emocionalmente y generen preferencia."""

    def create_strategy(self, brand: Dict[str, Any]) -> Dict[str, Any]:
        """Crea estrategia de marca"""
        return {"positioning": "", "identity": {}, "architecture": ""}

    def brand_audit(self, brand: str) -> Dict[str, Any]:
        """Audita marca existente"""
        return {"strengths": [], "weaknesses": [], "opportunities": []}
