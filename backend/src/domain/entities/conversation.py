from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class Conversation:
    id: Optional[int]
    user_id: int
    conversation_id: str
    title: str
    messages: List[Dict[str, Any]] = field(default_factory=list)
    model: Optional[str] = None
    agents: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(user_id: int, conversation_id: str, title: str, model: str, agents: List[str]) -> 'User':
        return Conversation(
            id=None,
            user_id=user_id,
            conversation_id=conversation_id,
            title=title,
            model=model,
            agents=agents
        )
    
    def add_message(self, role: str, content: str, agent: Optional[str] = None, sections: Optional[List] = None):
        self.messages.append({
            "role": role,
            "content": content,
            "agent": agent,
            "sections": sections or [],
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
