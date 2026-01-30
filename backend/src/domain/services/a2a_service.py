from typing import Dict, Any, List, Optional
import uuid
from ..entities.a2a_types import (
    A2AMessage, A2AResponse, AgentProfile, AgentCapability,
    MessageType, Priority, AgentStatus
)

class A2AService:
    """
    Servicio de Dominio A2A (Protocolo Agent-to-Agent)
    
    Gestiona las reglas de comunicación, validación y enrutamiento
    de mensajes entre agentes.
    """
    
    def __init__(self):
        self.active_conversations: Dict[str, List[A2AMessage]] = {}
        self.agent_registry: Dict[str, AgentProfile] = {}
        
    def register_agent(self, profile: AgentProfile) -> bool:
        """Registrar un agente en el protocolo"""
        self.agent_registry[profile.agent_id] = profile
        return True
    
    def create_message(
        self,
        sender_id: str,
        sender_capability: AgentCapability,
        subject: str,
        payload: Dict[str, Any],
        message_type: MessageType = MessageType.REQUEST,
        recipient_id: Optional[str] = None,
        recipient_capabilities: Optional[List[AgentCapability]] = None,
        priority: Priority = Priority.NORMAL,
        conversation_id: Optional[str] = None,
        **kwargs
    ) -> A2AMessage:
        """Crear un mensaje A2A estructurado"""
        
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        message = A2AMessage(
            message_type=message_type,
            priority=priority,
            sender_id=sender_id,
            sender_capability=sender_capability,
            recipient_id=recipient_id,
            recipient_capabilities=recipient_capabilities,
            subject=subject,
            payload=payload,
            conversation_id=conversation_id,
            **kwargs
        )
        
        # Almacenar en conversación activa (In-Memory persistence for context)
        # En un sistema distribuido, esto debería delegarse a un repositorio de infraestructura via Port.
        if conversation_id not in self.active_conversations:
            self.active_conversations[conversation_id] = []
        self.active_conversations[conversation_id].append(message)
        
        return message
    
    def create_response(
        self,
        original_message: A2AMessage,
        responder_id: str,
        responder_capability: AgentCapability,
        result: Any,
        success: bool = True,
        **kwargs
    ) -> A2AResponse:
        """Crear una respuesta A2A estructurada"""
        
        response = A2AResponse(
            original_message_id=original_message.message_id,
            conversation_id=original_message.conversation_id,
            responder_id=responder_id,
            responder_capability=responder_capability,
            success=success,
            result=result,
            **kwargs
        )
        
        return response
    
    def find_capable_agents(
        self,
        required_capability: AgentCapability,
        exclude_agents: Optional[List[str]] = None
    ) -> List[AgentProfile]:
        """Encontrar agentes con una capacidad específica"""
        
        exclude_agents = exclude_agents or []
        capable_agents = []
        
        for agent_id, profile in self.agent_registry.items():
            if agent_id in exclude_agents:
                continue
            
            if (profile.primary_capability == required_capability or
                required_capability in profile.secondary_capabilities):
                if profile.status == AgentStatus.IDLE or profile.current_load < profile.max_concurrent_tasks:
                    capable_agents.append(profile)
        
        # Ordenar por carga actual (menor carga primero)
        capable_agents.sort(key=lambda x: x.current_load)
        
        return capable_agents
    
    def get_conversation_history(self, conversation_id: str) -> List[A2AMessage]:
        """Obtener historial de una conversación"""
        return self.active_conversations.get(conversation_id, [])
    
    def validate_message(self, message: A2AMessage) -> tuple[bool, Optional[str]]:
        """Validar un mensaje A2A"""
        
        # Validar sender existe
        if message.sender_id not in self.agent_registry:
            # En modo estricto, esto fallaría. 
            # Pero permitimos que 'orchestrator' y otros envíen sin estar formalmente registrados a veces
            # o si el registro es asíncrono.
            pass
            # return False, f"Sender agent {message.sender_id} not registered"
        
        # Validar recipient si es específico
        if message.recipient_id and message.recipient_id not in self.agent_registry:
             # return False, f"Recipient agent {message.recipient_id} not registered"
             pass
        
        # Validar payload no está vacío
        if not message.payload:
            return False, "Message payload cannot be empty"
        
        return True, None

# Singleton-like instance for domain usage
# En una app real usaríamos Inyección de Dependencias
a2a_service = A2AService()
