from typing import List, Optional, Dict, Any
from src.domain.exceptions.domain_exceptions import ValidationException

class AgentId:
    def __init__(self, value: str):
        if not value or not value.isalnum():
            # Permitir guiones bajos por consistencia con AGENT_DEFINITIONS
            if not all(c.isalnum() or c == '_' for c in value):
                raise ValidationException(f"AgentId inválido: {value}")
        self._value = value

    def get_value(self) -> str:
        return self._value

    def __str__(self):
        return self._value

class ModelName:
    def __init__(self, value: str):
        if not value or "/" not in value and "-" not in value:
            # Validación básica para nombres de modelos como 'openai/gpt-4o' o 'llama-3'
            pass
        self._value = value

    def get_value(self) -> str:
        return self._value

    def __str__(self):
        return self._value

class AgentCapability:
    # Reutilizando conceptos de a2a_protocol pero como VO de dominio
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    WRITING = "writing"
    CODING = "coding"
    RESEARCH = "research"
    # ... otros según sea necesario
