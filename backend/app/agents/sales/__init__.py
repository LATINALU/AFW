"""
AFW v0.5.0 - Categoría: Ventas y Comercial
10 Agentes Especializados en Ventas
"""

from .sales_executive import SalesExecutiveAgent
from .account_manager import AccountManagerAgent
from .business_development import BusinessDevelopmentAgent
from .sales_engineer import SalesEngineerAgent
from .customer_success import CustomerSuccessAgent
from .sales_trainer import SalesTrainerAgent
from .proposal_writer import ProposalWriterAgent
from .sales_analyst import SalesAnalystAgent
from .channel_manager import ChannelManagerAgent
from .crm_specialist import CRMSpecialistAgent

SALES_AGENTS = [
    SalesExecutiveAgent, AccountManagerAgent, BusinessDevelopmentAgent,
    SalesEngineerAgent, CustomerSuccessAgent, SalesTrainerAgent,
    ProposalWriterAgent, SalesAnalystAgent, ChannelManagerAgent, CRMSpecialistAgent
]

__all__ = [
    "SalesExecutiveAgent", "AccountManagerAgent", "BusinessDevelopmentAgent",
    "SalesEngineerAgent", "CustomerSuccessAgent", "SalesTrainerAgent",
    "ProposalWriterAgent", "SalesAnalystAgent", "ChannelManagerAgent",
    "CRMSpecialistAgent", "SALES_AGENTS"
]
