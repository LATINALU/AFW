"""
AFW v0.5.0 - Categoría: Gestión de Proyectos
10 Agentes Especializados en Project Management
"""

from .project_manager import ProjectManagerAgent
from .scrum_master import ScrumMasterAgent
from .product_owner import ProductOwnerAgent
from .program_manager import ProgramManagerAgent
from .pmo_specialist import PMOSpecialistAgent
from .agile_coach import AgileCoachAgent
from .change_manager import ChangeManagerAgent
from .stakeholder_manager import StakeholderManagerAgent
from .resource_planner import ResourcePlannerAgent
from .portfolio_manager import PortfolioManagerAgent

PROJECT_MANAGEMENT_AGENTS = [
    ProjectManagerAgent, ScrumMasterAgent, ProductOwnerAgent,
    ProgramManagerAgent, PMOSpecialistAgent, AgileCoachAgent,
    ChangeManagerAgent, StakeholderManagerAgent, ResourcePlannerAgent,
    PortfolioManagerAgent
]

__all__ = [
    "ProjectManagerAgent", "ScrumMasterAgent", "ProductOwnerAgent",
    "ProgramManagerAgent", "PMOSpecialistAgent", "AgileCoachAgent",
    "ChangeManagerAgent", "StakeholderManagerAgent", "ResourcePlannerAgent",
    "PortfolioManagerAgent", "PROJECT_MANAGEMENT_AGENTS"
]
