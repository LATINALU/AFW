"""
AFW v0.5.0 - Categoría: Operaciones y Logística
10 Agentes Especializados en Operaciones
"""

from .operations_manager import OperationsManagerAgent
from .supply_chain_analyst import SupplyChainAnalystAgent
from .logistics_coordinator import LogisticsCoordinatorAgent
from .inventory_specialist import InventorySpecialistAgent
from .process_optimizer import ProcessOptimizerAgent
from .quality_assurance import QualityAssuranceAgent
from .procurement_specialist import ProcurementSpecialistAgent
from .warehouse_manager import WarehouseManagerAgent
from .distribution_planner import DistributionPlannerAgent
from .lean_specialist import LeanSpecialistAgent

OPERATIONS_AGENTS = [
    OperationsManagerAgent, SupplyChainAnalystAgent, LogisticsCoordinatorAgent,
    InventorySpecialistAgent, ProcessOptimizerAgent, QualityAssuranceAgent,
    ProcurementSpecialistAgent, WarehouseManagerAgent, DistributionPlannerAgent,
    LeanSpecialistAgent
]

__all__ = [
    "OperationsManagerAgent", "SupplyChainAnalystAgent", "LogisticsCoordinatorAgent",
    "InventorySpecialistAgent", "ProcessOptimizerAgent", "QualityAssuranceAgent",
    "ProcurementSpecialistAgent", "WarehouseManagerAgent", "DistributionPlannerAgent",
    "LeanSpecialistAgent", "OPERATIONS_AGENTS"
]
