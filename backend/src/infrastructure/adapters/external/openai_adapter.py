import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from src.domain.ports.output.llm_provider import LLMProviderPort

class OpenAILLMAdapter(LLMProviderPort):
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 4000,
        stream: bool = False
    ) -> Any:
        # Nota: En una implementación real, esto debería manejar el streaming si stream=True
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        if stream:
            return response
        
        return response.choices[0].message.content
