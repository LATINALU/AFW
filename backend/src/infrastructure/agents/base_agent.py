from typing import Dict, Any, List, Optional
from abc import abstractmethod
import time
from datetime import datetime

from ...domain.ports.input.agent_port import AgentPort
from ...domain.ports.output.llm_port import LLMProviderPort
from ...domain.entities.a2a_types import (
    A2AMessage, A2AResponse, AgentProfile, AgentCapability,
    MessageType, AgentStatus
)
from ...domain.services.a2a_service import a2a_service

# Default Adapter
from ...infrastructure.adapters.external.llm_adapter import LLMAdapter

class BaseAgent(AgentPort):
    """
    Implementación base de Agente (Infraestructura).
    Implementa el puerto AgentPort.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        primary_capability: AgentCapability,
        specialization: str,
        description: str,
        backstory: str = "",
        model_name: str = "gpt-4",
        level: int = 1,
        llm_provider: Optional[LLMProviderPort] = None
    ):
        self.profile = AgentProfile(
            agent_id=agent_id,
            name=name,
            primary_capability=primary_capability,
            specialization=specialization,
            description=description,
            backstory=backstory,
            model_name=model_name,
            level=level
        )
        self.llm_provider = llm_provider or LLMAdapter()
        
        # Register in A2A
        a2a_service.register_agent(self.profile)

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Prompt especializado"""
        pass

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Lógica por defecto: llamada simple al LLM con system prompt.
        Se puede sobreescribir.
        """
        # Token Optimization: Structure input clearly to avoid verbosity
        # Extract previous output if exists to avoid sending entire context dump
        prev_output = context.get("previous_agent_output", "") if context else ""
        
        user_input = task
        # If task already contains previous output (done in orchestrator), we might be duplicating.
        # Orchestrator sends task = "{prev}\n\nTask: {orig}".
        # So we just send 'task' in the user prompt.
        # But we should be careful about context['original_request'].
        
        # Minimized Context
        minimized_context = {
            k: v for k, v in (context or {}).items() 
            if k not in ["previous_agent_output", "original_request"]
        }
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": f"{task}\n\nMetaContext: {minimized_context}"}
        ]
        
        response_text = await self.llm_provider.chat_completion(
            messages=messages, 
            model=self.profile.model_name
        )
        
        return {"response": response_text}

    async def handle_message(self, message: A2AMessage) -> A2AResponse:
        """Manejo de mensajes A2A"""
        start_time = time.time()
        
        try:
            self.profile.status = AgentStatus.PROCESSING
            self.profile.current_load += 1
            
            result = {}
            if message.message_type == MessageType.REQUEST:
                task = message.payload.get("task") or message.payload.get("query")
                result = await self.process_task(task, message.context)
            
            processing_time = (time.time() - start_time) * 1000
            
            return a2a_service.create_response(
                original_message=message,
                responder_id=self.profile.agent_id,
                responder_capability=self.profile.primary_capability,
                result=result,
                success=True,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            return a2a_service.create_response(
                original_message=message,
                responder_id=self.profile.agent_id,
                responder_capability=self.profile.primary_capability,
                result={"error": str(e)},
                success=False,
                error_message=str(e)
            )
        finally:
            self.profile.current_load -= 1
            self.profile.status = AgentStatus.IDLE
            self.profile.last_active = datetime.utcnow()
