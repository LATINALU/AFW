"""
AFW v0.5.0 - Categoría: Desarrollo de Software
10 Agentes Especializados en Desarrollo y Tecnología
"""

from .fullstack_developer import FullstackDeveloperAgent
from .backend_architect import BackendArchitectAgent
from .frontend_specialist import FrontendSpecialistAgent
from .devops_engineer import DevOpsEngineerAgent
from .database_expert import DatabaseExpertAgent
from .security_specialist import SecuritySpecialistAgent
from .mobile_developer import MobileDeveloperAgent
from .qa_automation import QAAutomationAgent
from .code_reviewer import CodeReviewerAgent
from .tech_lead import TechLeadAgent

SOFTWARE_DEVELOPMENT_AGENTS = [
    FullstackDeveloperAgent,
    BackendArchitectAgent,
    FrontendSpecialistAgent,
    DevOpsEngineerAgent,
    DatabaseExpertAgent,
    SecuritySpecialistAgent,
    MobileDeveloperAgent,
    QAAutomationAgent,
    CodeReviewerAgent,
    TechLeadAgent
]

__all__ = [
    "FullstackDeveloperAgent",
    "BackendArchitectAgent", 
    "FrontendSpecialistAgent",
    "DevOpsEngineerAgent",
    "DatabaseExpertAgent",
    "SecuritySpecialistAgent",
    "MobileDeveloperAgent",
    "QAAutomationAgent",
    "CodeReviewerAgent",
    "TechLeadAgent",
    "SOFTWARE_DEVELOPMENT_AGENTS"
]
