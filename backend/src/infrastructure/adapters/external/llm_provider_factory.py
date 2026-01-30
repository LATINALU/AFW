from typing import Dict, Any
from src.domain.ports.output.llm_provider import LLMProviderPort, LLMProviderFactoryPort
from src.infrastructure.adapters.external.openai_adapter import OpenAILLMAdapter

class LLMProviderFactory(LLMProviderFactoryPort):
    def create(self, api_config: Dict[str, Any]) -> LLMProviderPort:
        api_type = api_config.get("type", "openai")
        api_key = api_config.get("api_key") or api_config.get("apiKey")
        base_url = api_config.get("base_url") or api_config.get("baseUrl")
        
        if api_type == "openai" or api_type == "groq":
            # Groq uses OpenAI compatible API if custom base_url is provided
            return OpenAILLMAdapter(api_key=api_key, base_url=base_url or "https://api.openai.com/v1")
        
        # Default to OpenAI adapter for now as it's the primary one
        return OpenAILLMAdapter(api_key=api_key, base_url=base_url)
