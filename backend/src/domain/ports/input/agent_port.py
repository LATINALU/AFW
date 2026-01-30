from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ...entities.a2a_types import A2AMessage, A2AResponse

class AgentPort(ABC):
    """
    Puerto de entrada para agentes.
    Define el comportamiento que todo agente debe exponer al dominio.
    """
    
    @abstractmethod
    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea específica"""
        pass
    
    @abstractmethod
    async def handle_message(self, message: A2AMessage) -> A2AResponse:
        """Maneja un mensaje del protocolo A2A"""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Obtiene el system prompt del agente"""
        pass
