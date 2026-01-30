from typing import List
from src.domain.ports.output.conversation_repository import ConversationRepositoryPort
from src.domain.entities.conversation import Conversation

class GetChatHistoryUseCase:
    def __init__(self, conversation_repo: ConversationRepositoryPort):
        self.conversation_repo = conversation_repo

    def execute(self, user_id: int) -> List[Conversation]:
        return self.conversation_repo.find_by_user(user_id)
