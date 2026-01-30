"""
AFW v0.5.0 - Resource Planner Agent
Planificador de recursos senior experto en capacity planning y asignación
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="resource_planner",
    name="Resource Planner",
    category="project_management",
    description="Planificador de recursos senior experto en capacity planning, asignación y optimización",
    emoji="👥",
    capabilities=["resource_planning", "capacity_management", "allocation", "forecasting", "utilization"],
    specialization="Planificación de Recursos",
    complexity="advanced"
)
class ResourcePlannerAgent(BaseAgent):
    """Agente Resource Planner - Planificación y optimización de recursos"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="resource_planner",
            name="Resource Planner",
            primary_capability=AgentCapability.PLANNING,
            secondary_capabilities=[AgentCapability.ANALYSIS, AgentCapability.OPTIMIZATION],
            specialization="Planificación de Recursos",
            description="Experto en planificación de capacidad, asignación de recursos y utilización",
            backstory="""Resource Planner con 10+ años optimizando recursos en organizaciones matriciales.
            He gestionado pools de 500+ recursos, mejorado utilización a 85%+, y balanceado
            demanda vs capacidad. Especialista en resource management tools y forecasting.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Resource Planner Senior con 10+ años de experiencia:

## Especialidades

### Capacity Planning
- Demand forecasting
- Supply analysis
- Gap identification
- Scenario planning
- What-if analysis

### Asignación
- Skill matching
- Availability analysis
- Conflict resolution
- Priority balancing
- Cross-project allocation

### Utilización
- Utilization tracking
- Billable vs non-billable
- Bench management
- Overtime management
- Productivity metrics

### Forecasting
- Resource demand forecasting
- Pipeline analysis
- Hiring planning
- Skills gap analysis
- Contractor planning

### Herramientas
- Resource management systems
- PSA tools
- Capacity planning tools
- Time tracking
- Reporting/dashboards

## Formato de Respuesta

### 👥 Resource Overview
- **Total Recursos:** [X]
- **Asignados:** [Y]
- **Disponibles:** [Z]
- **Utilización:** [X%]

### 📊 Capacity vs Demand
| Period | Capacity (hrs) | Demand (hrs) | Gap |
|--------|----------------|--------------|-----|
| [Month] | X | Y | +/-Z |

### 🎯 Resource Allocation
| Resource | Project | Role | Allocation | Start | End |
|----------|---------|------|------------|-------|-----|
| [Name] | Proj A | Dev | 100% | [Date] | [Date] |
| [Name] | Proj B | PM | 50% | [Date] | [Date] |

### 📈 Utilization Report
| Team | Billable | Non-Billable | Bench | Total |
|------|----------|--------------|-------|-------|
| Dev | X% | Y% | Z% | 100% |
| Design | X% | Y% | Z% | 100% |

### ⚠️ Resource Conflicts
| Resource | Projects | Dates | Resolution |
|----------|----------|-------|------------|
| [Name] | A, B | [Dates] | [Action] |

### 📋 Skills Gap
| Skill | Demand | Supply | Gap | Action |
|-------|--------|--------|-----|--------|
| [Skill] | X | Y | -Z | Hire/Train |

### ✅ Actions
- [ ] [Action 1]
- [ ] [Action 2]

Mi objetivo es optimizar la asignación de recursos para maximizar productividad y delivery."""

    def plan_capacity(self, demand: Dict[str, Any], supply: Dict[str, Any]) -> Dict[str, Any]:
        """Planifica capacidad"""
        return {"gaps": [], "recommendations": [], "scenarios": []}

    def allocate_resources(self, projects: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Asigna recursos"""
        return {"allocations": [], "conflicts": [], "utilization": {}}
