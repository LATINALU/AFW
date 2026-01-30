"""
AFW v0.5.0 - Agent Registry
Registro centralizado de agentes
"""

from typing import Dict, Any, List, Optional

# Registro global de agentes
AGENT_REGISTRY: Dict[str, Any] = {}

def register_agent_class(agent_class):
    """Registrar una clase de agente"""
    if hasattr(agent_class, '_agent_metadata'):
        metadata = agent_class._agent_metadata
        AGENT_REGISTRY[metadata['agent_id']] = {
            'class': agent_class,
            'metadata': metadata
        }

def get_registered_agents() -> Dict[str, Any]:
    """Obtener todos los agentes registrados"""
    return AGENT_REGISTRY

def get_agent_by_id(agent_id: str) -> Optional[Any]:
    """Obtener un agente por su ID"""
    return AGENT_REGISTRY.get(agent_id)

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
    """Decorador para registrar agentes"""
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
        register_agent_class(cls)
        return cls
    return decorator

class AgentCategory:
    """Clase para representar categorías de agentes"""
    def __init__(self, name: str, description: str, emoji: str):
        self.name = name
        self.description = description
        self.emoji = emoji
