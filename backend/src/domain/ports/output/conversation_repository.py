from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.conversation import Conversation

class ConversationRepositoryPort(ABC):
    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        pass

    @abstractmethod
    def find_by_conversation_id(self, conv_id: str, user_id: int) -> Optional[Conversation]:
        pass

    @abstractmethod
    def find_by_user(self, user_id: int) -> List[Conversation]:
        pass

    @abstractmethod
    def delete(self, conv_id: str, user_id: int) -> bool:
        pass
