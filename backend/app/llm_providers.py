"""
Proveedores de LLM para ATP v1.0.1
Usa OpenAI SDK directamente - compatible con múltiples proveedores
"""
import os
from openai import OpenAI
from typing import Optional, Dict, Any, List
from app.config import MODELS, GROQ_API_KEY

# Configuración de proveedores con sus endpoints y modelos por defecto
PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4o-mini",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "model": "mistral-large-latest",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2",
    },
}


def get_openai_client(api_config: Dict[str, Any] = None) -> tuple[OpenAI, str]:
    """
    Obtiene un cliente OpenAI configurado y el modelo a usar.
    Retorna (client, model_name)
    """
    if api_config and api_config.get("api_key"):
        api_type = api_config.get("type", "openai")
        api_key = api_config.get("api_key", "")
        custom_base_url = api_config.get("base_url")
        
        provider_config = PROVIDERS.get(api_type, PROVIDERS["openai"])
        base_url = custom_base_url or provider_config["base_url"]
        model = provider_config["model"]
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        return client, model
    
    # Fallback a variables de entorno (solo Groq)
    if GROQ_API_KEY:
        client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        return client, "llama-3.3-70b-versatile"
    else:
        raise ValueError("No API key configured. Please add your API key in Settings.")


async def chat_completion(
    messages: List[Dict[str, str]], 
    model: str = None,
    api_config: Dict[str, Any] = None,
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> str:
    """
    Ejecuta una llamada de chat completion y retorna el contenido.
    """
    client, default_model = get_openai_client(api_config)
    
    # Usar el modelo proporcionado o el default
    actual_model = model or default_model
    
    response = client.chat.completions.create(
        model=actual_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    return response.choices[0].message.content


async def test_connection(api_config: Dict[str, Any] = None) -> bool:
    """Prueba la conexión con el modelo"""
    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": "Responde solo 'OK'"}],
            api_config=api_config,
            max_tokens=10
        )
        return "OK" in result or len(result) > 0
    except Exception as e:
        print(f"Error testing connection: {e}")
        return False
