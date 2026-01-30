from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from datetime import datetime
from src.domain.value_objects.agent_vo import AgentId, ModelName
from src.domain.ports.output.llm_provider import LLMProviderPort

@dataclass
class AgentProfile:
    """Perfil completo de un agente especializado (Domain Entity)"""
    agent_id: str
    name: str
    description: str
    level: int
    specialization: str
    backstory: str
    model: str
    system_prompt: str
    primary_capability: str = "general"
    capabilities: List[str] = field(default_factory=list)
    version: str = "0.8.0"
    expertise_level: str = "expert"
    status: str = "idle"
    current_load: int = 0
    max_concurrent_tasks: int = 3
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)

class Agent:
    def __init__(self, profile: AgentProfile, llm_provider: LLMProviderPort):
        self.profile = profile
        self.llm_provider = llm_provider

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea usando el proveedor de LLM configurado"""
        
        # Preparar mensajes
        messages = [
            {"role": "system", "content": self.profile.system_prompt},
            {"role": "user", "content": self._format_user_message(task, context)}
        ]
        
        try:
            response = await self.llm_provider.chat_completion(
                messages=messages,
                model=self.profile.model
            )
            
            return {
                "agent_id": self.profile.agent_id,
                "agent_name": self.profile.name,
                "content": response,
                "status": "completed"
            }
        except Exception as e:
            return {
                "agent_id": self.profile.agent_id,
                "agent_name": self.profile.name,
                "content": f"Error: {str(e)}",
                "status": "error"
            }

    def _format_user_message(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        context_str = str(context) if context else "None"
        return f"Task: {task}\n\nContext: {context_str}"
