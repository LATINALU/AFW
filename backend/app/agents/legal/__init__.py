"""
AFW v0.5.0 - Categoría: Legal y Compliance
10 Agentes Especializados en Derecho y Cumplimiento
"""

from .corporate_lawyer import CorporateLawyerAgent
from .contract_specialist import ContractSpecialistAgent
from .compliance_officer import ComplianceOfficerAgent
from .intellectual_property import IntellectualPropertyAgent
from .labor_law_expert import LaborLawExpertAgent
from .data_privacy_officer import DataPrivacyOfficerAgent
from .litigation_specialist import LitigationSpecialistAgent
from .regulatory_advisor import RegulatoryAdvisorAgent
from .legal_researcher import LegalResearcherAgent
from .paralegal_assistant import ParalegalAssistantAgent

LEGAL_AGENTS = [
    CorporateLawyerAgent, ContractSpecialistAgent, ComplianceOfficerAgent,
    IntellectualPropertyAgent, LaborLawExpertAgent, DataPrivacyOfficerAgent,
    LitigationSpecialistAgent, RegulatoryAdvisorAgent, LegalResearcherAgent,
    ParalegalAssistantAgent
]

__all__ = [
    "CorporateLawyerAgent", "ContractSpecialistAgent", "ComplianceOfficerAgent",
    "IntellectualPropertyAgent", "LaborLawExpertAgent", "DataPrivacyOfficerAgent",
    "LitigationSpecialistAgent", "RegulatoryAdvisorAgent", "LegalResearcherAgent",
    "ParalegalAssistantAgent", "LEGAL_AGENTS"
]
