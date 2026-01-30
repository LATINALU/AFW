"""
Endpoint para detectar modelos disponibles en una API
"""
import httpx
from typing import List, Dict, Any, Optional

# Descripciones de para qué es buena cada IA
MODEL_DESCRIPTIONS = {
    # OpenAI
    "gpt-4o": "🧠 Mejor para: Razonamiento complejo, análisis profundo, código avanzado",
    "gpt-4o-mini": "⚡ Mejor para: Tareas rápidas, chat, resúmenes, bajo costo",
    "gpt-4-turbo": "💪 Mejor para: Tareas largas, documentos extensos, visión",
    "gpt-3.5-turbo": "💰 Mejor para: Tareas simples, alto volumen, económico",
    "o1-preview": "🔬 Mejor para: Matemáticas, ciencia, razonamiento paso a paso",
    "o1-mini": "🧮 Mejor para: Código, lógica, problemas técnicos",
    
    # Groq (Llama)
    "llama-3.3-70b-versatile": "🦙 Mejor para: Uso general, rápido, multilingüe",
    "llama-3.1-70b-versatile": "🦙 Mejor para: Razonamiento, código, análisis",
    "llama-3.1-8b-instant": "⚡ Mejor para: Respuestas ultra rápidas, chat",
    "llama-guard-3-8b": "🛡️ Mejor para: Moderación de contenido, seguridad",
    "mixtral-8x7b-32768": "🎭 Mejor para: Contexto largo, multilingüe",
    "gemma-7b-it": "💎 Mejor para: Instrucciones, tareas específicas",
    "gemma2-9b-it": "💎 Mejor para: Razonamiento mejorado, código",
    
    # DeepSeek
    "deepseek-chat": "🔍 Mejor para: Chat general, código, análisis",
    "deepseek-coder": "💻 Mejor para: Programación, debugging, código",
    "deepseek-reasoner": "🧠 Mejor para: Razonamiento profundo, matemáticas",
    
    # Anthropic Claude
    "claude-3-5-sonnet-20241022": "✨ Mejor para: Escritura, análisis, código elegante",
    "claude-3-opus-20240229": "👑 Mejor para: Tareas complejas, creatividad, investigación",
    "claude-3-sonnet-20240229": "📝 Mejor para: Balance calidad/velocidad, documentos",
    "claude-3-haiku-20240307": "🚀 Mejor para: Respuestas rápidas, alto volumen",
    
    # Mistral
    "mistral-large-latest": "🌟 Mejor para: Razonamiento, multilingüe europeo",
    "mistral-medium-latest": "⚖️ Mejor para: Balance costo/rendimiento",
    "mistral-small-latest": "💨 Mejor para: Tareas simples, rápido",
    "codestral-latest": "💻 Mejor para: Código, 80+ lenguajes",
    
    # Together AI
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": "🦙 Mejor para: Instrucciones, chat, análisis",
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": "🏆 Mejor para: Máxima calidad, tareas complejas",
    "mistralai/Mixtral-8x22B-Instruct-v0.1": "🎭 Mejor para: Contexto largo, multilingüe",
    "Qwen/Qwen2.5-72B-Instruct-Turbo": "🐉 Mejor para: Chino/inglés, código, matemáticas",
    
    # OpenRouter
    "openai/gpt-4o": "🧠 Mejor para: Razonamiento complejo, análisis",
    "anthropic/claude-3.5-sonnet": "✨ Mejor para: Escritura, código elegante",
    "google/gemini-pro-1.5": "🌐 Mejor para: Multimodal, contexto muy largo",
    "meta-llama/llama-3.1-405b-instruct": "🏆 Mejor para: Open source más potente",
}


async def fetch_available_models(api_type: str, api_key: str, base_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Consulta la API para obtener los modelos disponibles.
    Retorna lista de modelos con nombre y descripción.
    """
    # Endpoints por proveedor
    endpoints = {
        "openai": "https://api.openai.com/v1/models",
        "groq": "https://api.groq.com/openai/v1/models",
        "deepseek": "https://api.deepseek.com/v1/models",
        "together": "https://api.together.xyz/v1/models",
        "openrouter": "https://openrouter.ai/api/v1/models",
        "mistral": "https://api.mistral.ai/v1/models",
        "ollama": "http://localhost:11434/v1/models",
    }
    
    url = base_url or endpoints.get(api_type, endpoints["openai"])
    if not url.endswith("/models"):
        url = url.rstrip("/") + "/models"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            models_data = data.get("data", data.get("models", []))
            
            models = []
            for model in models_data:
                model_id = model.get("id", model.get("name", ""))
                if not model_id:
                    continue
                    
                # Filtrar solo modelos de chat/completions
                if any(skip in model_id.lower() for skip in ["embed", "whisper", "tts", "dall-e", "moderation"]):
                    continue
                
                description = MODEL_DESCRIPTIONS.get(model_id, "🤖 Modelo de IA")
                
                models.append({
                    "id": model_id,
                    "name": model_id,
                    "description": description,
                    "provider": api_type,
                })
            
            # Ordenar por nombre
            models.sort(key=lambda x: x["name"])
            return models
            
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def get_model_description(model_id: str) -> str:
    """Obtiene la descripción de un modelo."""
    return MODEL_DESCRIPTIONS.get(model_id, "🤖 Modelo de IA para tareas generales")
