"""
AFW v0.5.0 - Categoría: Recursos Humanos
10 Agentes Especializados en RRHH y Gestión del Talento
"""

from .recruiter import RecruiterAgent
from .talent_development import TalentDevelopmentAgent
from .compensation_analyst import CompensationAnalystAgent
from .employee_relations import EmployeeRelationsAgent
from .training_coordinator import TrainingCoordinatorAgent
from .performance_manager import PerformanceManagerAgent
from .hr_analytics import HRAnalyticsAgent
from .onboarding_specialist import OnboardingSpecialistAgent
from .culture_champion import CultureChampionAgent
from .benefits_administrator import BenefitsAdministratorAgent

HUMAN_RESOURCES_AGENTS = [
    RecruiterAgent, TalentDevelopmentAgent, CompensationAnalystAgent,
    EmployeeRelationsAgent, TrainingCoordinatorAgent, PerformanceManagerAgent,
    HRAnalyticsAgent, OnboardingSpecialistAgent, CultureChampionAgent,
    BenefitsAdministratorAgent
]

__all__ = [
    "RecruiterAgent", "TalentDevelopmentAgent", "CompensationAnalystAgent",
    "EmployeeRelationsAgent", "TrainingCoordinatorAgent", "PerformanceManagerAgent",
    "HRAnalyticsAgent", "OnboardingSpecialistAgent", "CultureChampionAgent",
    "BenefitsAdministratorAgent", "HUMAN_RESOURCES_AGENTS"
]
