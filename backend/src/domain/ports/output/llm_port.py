from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMProviderPort(ABC):
    """
    Puerto de salida para proveedores de LLM.
    Interface que debe ser implementada por la infraestructura.
    """
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        api_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Genera una respuesta de chat usando el LLM.
        """
        pass
