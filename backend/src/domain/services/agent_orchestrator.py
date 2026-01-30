from typing import List, Dict, Any, Optional
from src.domain.entities.agent import Agent, AgentProfile
from src.domain.value_objects.agent_vo import AgentId, ModelName

class AgentOrchestratorService:
    """Servicio de dominio para orquestar la ejecución de múltiples agentes"""
    
    def __init__(self, agents_map: Dict[str, Any]):
        self.agents_map = agents_map

    async def execute_pipeline(self, task: str, selected_agents: List[str], model: str, context: Dict[str, Any]):
        results = []
        for agent_id in selected_agents:
            if agent_id in self.agents_map:
                # En un diseño hexagonal real, esto llamaría a un puerto que el adaptador de infra implementa
                # Para esta migración, mantenemos la lógica de orquestación centralizada aquí
                result = await self.agents_map[agent_id].process_task(task, context)
                results.append(result)
        return results

# AFW v0.5.0 - Importar definiciones desde el nuevo registry centralizado
from app.agents.registry import AGENT_DEFINITIONS, CATEGORIES, get_agents_by_category, get_all_categories
