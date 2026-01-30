"""
AFW v0.5.0 - Categoría: Finanzas y Contabilidad
10 Agentes Especializados en Finanzas
"""

from .financial_analyst import FinancialAnalystAgent
from .accountant import AccountantAgent
from .tax_specialist import TaxSpecialistAgent
from .investment_advisor import InvestmentAdvisorAgent
from .budget_planner import BudgetPlannerAgent
from .auditor import AuditorAgent
from .payroll_specialist import PayrollSpecialistAgent
from .financial_controller import FinancialControllerAgent
from .risk_analyst import RiskAnalystAgent
from .treasury_manager import TreasuryManagerAgent

FINANCE_AGENTS = [
    FinancialAnalystAgent, AccountantAgent, TaxSpecialistAgent,
    InvestmentAdvisorAgent, BudgetPlannerAgent, AuditorAgent,
    PayrollSpecialistAgent, FinancialControllerAgent, RiskAnalystAgent,
    TreasuryManagerAgent
]

__all__ = [
    "FinancialAnalystAgent", "AccountantAgent", "TaxSpecialistAgent",
    "InvestmentAdvisorAgent", "BudgetPlannerAgent", "AuditorAgent",
    "PayrollSpecialistAgent", "FinancialControllerAgent", "RiskAnalystAgent",
    "TreasuryManagerAgent", "FINANCE_AGENTS"
]
