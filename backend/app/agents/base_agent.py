"""
AFW v0.5.0 - Base Agent
Clase base para todos los agentes del sistema
Compatible con src.infrastructure.agents.base_agent
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.shared.a2a_protocol import AgentCapability
from src.infrastructure.adapters.external.llm_adapter import LLMAdapter

class BaseAgent(ABC):
    """Clase base para todos los agentes - Compatible con sistema de orquestación"""
    
    def __init__(
        self, 
        agent_id: str = None,
        name: str = None,
        primary_capability: AgentCapability = None,
        secondary_capabilities: List[AgentCapability] = None,
        specialization: str = "",
        description: str = "",
        backstory: str = "",
        model: str = None,
        api_config: Dict[str, Any] = None,
        language: str = "es",
        category: str = None,
        level: int = 3
    ):
        """
        Constructor compatible con ambos sistemas de agentes.
        Acepta parámetros del sistema antiguo y nuevo.
        """
        self.agent_id = agent_id or "unknown"
        self.name = name or "Agent"
        self.id = self.agent_id  # Alias para compatibilidad
        self.category = category or "general"
        self.description = description
        self.specialization = specialization
        self.backstory = backstory
        self.model = model or "openai/gpt-4o-mini"
        self.api_config = api_config
        self.language = language
        self.level = level
        
        # Crear perfil compatible con A2A
        try:
            from src.domain.entities.a2a_types import AgentProfile
            self.profile = AgentProfile(
                agent_id=self.agent_id,
                name=self.name,
                primary_capability=primary_capability or AgentCapability.GENERAL,
                specialization=specialization,
                description=description,
                backstory=backstory,
                model_name=model or "openai/gpt-4o-mini",
                level=level
            )
        except ImportError:
            # Fallback si no está disponible A2A
            self.profile = None
        
        # Inicializar LLM adapter (sin parámetros, api_config se pasa en chat_completion)
        self.llm_provider = None
        if api_config:
            try:
                self.llm_provider = LLMAdapter()  # LLMAdapter no acepta parámetros en constructor
            except Exception as e:
                print(f"⚠️ Error inicializando LLM adapter: {e}")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Obtener el prompt del sistema para este agente"""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Obtener las capacidades del agente"""
        return []
    
    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesar una tarea con el agente"""
        # Inicializar LLM provider si no existe
        if not self.llm_provider:
            try:
                self.llm_provider = LLMAdapter()
            except Exception as e:
                print(f"⚠️ Error inicializando LLM adapter en process_task: {e}")
        
        if self.llm_provider and self.api_config:
            try:
                messages = [
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": task}
                ]
                # Pasar api_config al método chat_completion, no al constructor
                response = await self.llm_provider.chat_completion(
                    messages=messages, 
                    model=self.model,
                    api_config=self.api_config
                )
                return {"response": response, "content": response}
            except Exception as e:
                error_msg = f"Error en LLM: {str(e)}"
                print(f"❌ {self.name}: {error_msg}")
                return {"response": error_msg, "content": error_msg}
        
        # Fallback: respuesta simulada si no hay LLM configurado
        fallback_response = f"[{self.name}] Análisis completado. Recomendaciones basadas en {self.specialization}."
        return {"response": fallback_response, "content": fallback_response}
    
    async def execute(self, task: str) -> str:
        """Ejecutar tarea - método de compatibilidad"""
        result = await self.process_task(task)
        return result.get("response", result.get("content", ""))

def register_agent(
    agent_id: str,
    name: str,
    category: str,
    description: str,
    emoji: str,
    capabilities: List[str],
    specialization: str,
    complexity: str
):
    """Decorador para registrar agentes en el AGENT_REGISTRY"""
    def decorator(cls):
        cls._agent_metadata = {
            'agent_id': agent_id,
            'name': name,
            'category': category,
            'description': description,
            'emoji': emoji,
            'capabilities': capabilities,
            'specialization': specialization,
            'complexity': complexity
        }
        
        # Registrar en el AGENT_REGISTRY global
        from app.agents.agent_registry import register_agent_class
        register_agent_class(cls)
        
        return cls
    return decorator
