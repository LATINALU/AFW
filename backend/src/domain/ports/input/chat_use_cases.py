from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SaveConversationInputDTO:
    user_id: int
    conversation_id: str
    title: str
    messages: List[Dict[str, Any]]
    model: str
    agents: List[str]

class SaveConversationUseCasePort(ABC):
    @abstractmethod
    async def execute(self, input: SaveConversationInputDTO) -> None:
        pass

class GetChatHistoryUseCasePort(ABC):
    @abstractmethod
    def execute(self, user_id: int) -> List[Any]:
        pass
    
class DeleteConversationUseCasePort(ABC):
    @abstractmethod
    def execute(self, conv_id: str, user_id: int) -> bool:
        pass
