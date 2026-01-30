from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ExecuteTaskInputDTO:
    task: str
    selected_agents: List[str]
    model: str
    api_config: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None

@dataclass
class AgentResultDTO:
    agent_id: str
    agent_name: str
    content: str
    status: str

class ExecuteTaskUseCasePort(ABC):
    @abstractmethod
    async def execute(self, input: ExecuteTaskInputDTO) -> List[AgentResultDTO]:
        pass
