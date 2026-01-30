from datetime import datetime
from src.domain.ports.input.chat_use_cases import SaveConversationUseCasePort, SaveConversationInputDTO
from src.domain.ports.output.conversation_repository import ConversationRepositoryPort
from src.domain.entities.conversation import Conversation

class SaveConversationUseCase(SaveConversationUseCasePort):
    def __init__(self, conversation_repo: ConversationRepositoryPort):
        self.conversation_repo = conversation_repo

    async def execute(self, input_data: SaveConversationInputDTO) -> None:
        # Lógica de orquestación
        # 1. Intentar encontrar conversación existente
        conversation = self.conversation_repo.find_by_conversation_id(
            input_data.conversation_id, 
            input_data.user_id
        )
        
        if not conversation:
            # 2. Crear nueva si no existe
            conversation = Conversation(
                id=None,
                user_id=input_data.user_id,
                conversation_id=input_data.conversation_id,
                title=input_data.title,
                messages=input_data.messages,
                model=input_data.model,
                agents=input_data.agents,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        else:
            # 3. Actualizar existente - Concatenar mensajes
            existing_messages = conversation.messages or []
            conversation.messages = existing_messages + input_data.messages
            conversation.title = input_data.title
            conversation.updated_at = datetime.now()
            
        # 4. Persistir a través del puerto
        self.conversation_repo.save(conversation)
