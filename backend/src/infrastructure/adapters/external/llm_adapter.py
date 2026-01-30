from typing import List, Dict, Any, Optional
from openai import OpenAI
from ....domain.ports.output.llm_port import LLMProviderPort
from ...config.settings import MODELS, GROQ_API_KEY

class LLMAdapter(LLMProviderPort):
    """
    Implementación del puerto LLMProviderPort usando OpenAI SDK.
    """
    
    def __init__(self):
        pass

    def _get_client(self, api_config: Optional[Dict[str, Any]] = None):
        """
        Obtiene un cliente OpenAI configurado.
        """
        api_key = None
        base_url = None
        model = "gpt-4o-mini"
        
        if api_config and api_config.get("api_key"):
            api_key = api_config.get("api_key")
            base_url = api_config.get("base_url")
            # Determine provider defaults if needed
            api_type = api_config.get("type", "openai")
            # (Logic to set default base_url if not provided based on type could go here)
        elif GROQ_API_KEY:
            api_key = GROQ_API_KEY
            base_url = "https://api.groq.com/openai/v1"
            model = "llama-3.3-70b-versatile"
        
        if not api_key:
            raise ValueError("No API key configured.")
            
        client = OpenAI(api_key=api_key, base_url=base_url)
        return client, model

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 4096,
        api_config: Optional[Dict[str, Any]] = None
    ) -> str:
        
        client, default_model = self._get_client(api_config)
        actual_model = model or default_model
        
        # Async call is not natively supported by OpenAI sync client without wrapping or using AsyncOpenAI
        # For simplicity in this synchronous context (or if we switch to AsyncOpenAI):
        # We should use AsyncOpenAI for async context.
        
        from openai import AsyncOpenAI
        
        # Re-instantiate as Async
        # Note: This is a bit inefficient, better to cache clients.
        # But for now, following the pattern:
        
        api_key = client.api_key
        base_url = str(client.base_url) 
        
        async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        
        response = await async_client.chat.completions.create(
            model=actual_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.choices[0].message.content
