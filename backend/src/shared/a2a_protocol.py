"""
A2A Protocol (Agent-to-Agent Communication Protocol)
Version: 0.8.0 - Shared Kernel (No Frameworks)
"""
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from enum import Enum
import uuid
from dataclasses import dataclass, field
from src.domain.entities.agent import AgentProfile

class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    QUERY = "query"
    COMMAND = "command"
    EVENT = "event"
    ERROR = "error"
    ACKNOWLEDGMENT = "ack"

class AgentCapability(str, Enum):
    REASONING = "reasoning"
    PLANNING = "planning"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    CRITICAL_THINKING = "critical_thinking"
    PROBLEM_SOLVING = "problem_solving"
    DECISION_MAKING = "decision_making"
    CODING = "coding"
    DATA_ANALYSIS = "data_analysis"
    DATA = "data"
    SYSTEM_ARCHITECTURE = "system_architecture"
    OPTIMIZATION = "optimization"
    SECURITY = "security"
    TECHNICAL = "technical"
    INTEGRATION = "integration"
    WRITING = "writing"
    COMMUNICATION = "communication"
    TRANSLATION = "translation"
    DOCUMENTATION = "documentation"
    PRESENTATION = "presentation"
    FORMATTING = "formatting"
    SUMMARY = "summary"
    QA = "qa"
    REVIEW = "review"
    VALIDATION = "validation"
    COORDINATION = "coordination"
    LEGAL = "legal"
    FINANCIAL = "financial"
    MEDICAL = "medical"
    SCIENTIFIC = "scientific"
    CREATIVE = "creative"
    EDUCATIONAL = "educational"
    MARKETING = "marketing"
    RESEARCH = "research"
    STATISTICS = "statistics"
    COMPLIANCE = "compliance"
    RISK = "risk"
    EXPLANATION = "explanation"

class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"

class AgentStatus(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class A2AMessage:
    sender_id: str
    sender_capability: str
    subject: str
    payload: Dict[str, Any]
    message_type: MessageType = MessageType.REQUEST
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: Priority = Priority.NORMAL
    recipient_id: Optional[str] = None
    recipient_capabilities: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    requires_response: bool = True
    timeout_seconds: Optional[int] = 30
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class A2AResponse:
    original_message_id: str
    conversation_id: str
    responder_id: str
    responder_capability: str
    success: bool
    result: Any
    response_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    status_code: int = 200
    reasoning: Optional[str] = None
    confidence: float = 1.0
    processing_time_ms: Optional[float] = None
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None
    suggestions: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class A2AProtocol:
    def __init__(self):
        self.active_conversations: Dict[str, List[A2AMessage]] = {}
        self.agent_registry: Dict[str, AgentProfile] = {}
        
    def register_agent(self, profile: AgentProfile) -> bool:
        self.agent_registry[profile.agent_id] = profile
        return True
    
    def create_message(
        self,
        sender_id: str,
        sender_capability: str,
        subject: str,
        payload: Dict[str, Any],
        message_type: MessageType = MessageType.REQUEST,
        recipient_id: Optional[str] = None,
        recipient_capabilities: Optional[List[str]] = None,
        priority: Priority = Priority.NORMAL,
        conversation_id: Optional[str] = None,
        **kwargs
    ) -> A2AMessage:
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        message = A2AMessage(
            sender_id=sender_id,
            sender_capability=sender_capability,
            subject=subject,
            payload=payload,
            message_type=message_type,
            recipient_id=recipient_id,
            recipient_capabilities=recipient_capabilities,
            priority=priority,
            conversation_id=conversation_id,
            **kwargs
        )
        
        if conversation_id not in self.active_conversations:
            self.active_conversations[conversation_id] = []
        self.active_conversations[conversation_id].append(message)
        
        return message
    
    def create_response(
        self,
        original_message: A2AMessage,
        responder_id: str,
        responder_capability: str,
        result: Any,
        success: bool = True,
        **kwargs
    ) -> A2AResponse:
        return A2AResponse(
            original_message_id=original_message.message_id,
            conversation_id=original_message.conversation_id,
            responder_id=responder_id,
            responder_capability=responder_capability,
            success=success,
            result=result,
            **kwargs
        )

a2a_protocol = A2AProtocol()
