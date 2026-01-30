from src.infrastructure.adapters.persistence.sqlite_conversation_repository import SQLiteConversationRepository
from src.infrastructure.adapters.persistence.sqlite_user_repository import SQLiteUserRepository
from src.infrastructure.adapters.persistence.in_memory_agent_repository import InMemoryAgentRepository
from src.infrastructure.adapters.external.openai_adapter import OpenAILLMAdapter
from src.application.use_cases.get_chat_history import GetChatHistoryUseCase
from src.application.use_cases.save_conversation import SaveConversationUseCase
from src.application.use_cases.auth_use_cases import LoginUseCase, RegisterUseCase
from src.application.use_cases.execute_task import ExecuteTaskUseCase
from src.shared.password_hasher import PBKDF2PasswordHasher
from app.config import OPENAI_API_KEY, GROQ_API_KEY

# Configuración de base de datos
DB_PATH = "atp_platform.db"

# Singletons de Infraestructura
from src.infrastructure.adapters.external.llm_provider_factory import LLMProviderFactory
from src.infrastructure.adapters.external.langgraph_orchestrator import LangGraphOrchestratorAdapter

# Singletons de Infraestructura
conversation_repo = SQLiteConversationRepository(DB_PATH)
user_repo = SQLiteUserRepository(DB_PATH)
agent_repo = InMemoryAgentRepository()
hasher = PBKDF2PasswordHasher()
workflow_adapter = LangGraphOrchestratorAdapter() # Use the new adapter
llm_factory = LLMProviderFactory()

# LLM Provider default
if GROQ_API_KEY:
    default_llm_provider = OpenAILLMAdapter(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
else:
    default_llm_provider = OpenAILLMAdapter(api_key=OPENAI_API_KEY or "no-key")

# Inyectores de Casos de Uso
def get_history_use_case():
    return GetChatHistoryUseCase(conversation_repo)

def get_save_conversation_use_case():
    return SaveConversationUseCase(conversation_repo)

def get_login_use_case():
    return LoginUseCase(user_repo, hasher)

def get_register_use_case():
    return RegisterUseCase(user_repo, hasher)

def get_execute_task_use_case():
    return ExecuteTaskUseCase(agent_repo, default_llm_provider, workflow_adapter, llm_factory)

def get_user_repository():
    return user_repo

def get_agent_repository():
    return agent_repo
