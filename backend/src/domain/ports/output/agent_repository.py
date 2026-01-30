from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.agent import AgentProfile

class AgentRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, agent_id: str) -> Optional[AgentProfile]:
        pass

    @abstractmethod
    def get_all(self) -> List[AgentProfile]:
        pass
