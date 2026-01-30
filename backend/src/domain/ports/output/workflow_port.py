from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.domain.entities.agent import Agent

class GraphWorkflowPort(ABC):
    @abstractmethod
    async def run_workflow(
        self, 
        task: str, 
        agents: List[Agent], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass
