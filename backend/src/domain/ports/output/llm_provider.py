from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMProviderPort(ABC):
    @abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 4000,
        stream: bool = False
    ) -> Any:
        pass

class LLMProviderFactoryPort(ABC):
    @abstractmethod
    def create(self, api_config: Dict[str, Any]) -> LLMProviderPort:
        pass
