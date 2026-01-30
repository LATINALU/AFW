"""
AFW v0.5.0 - Agents For Works
Configuración del backend con soporte para múltiples proveedores de IA.
Groq como proveedor predeterminado, con soporte para APIs locales y otros proveedores.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY")  # Para APIs locales

# Model configurations - Solo los 2 modelos disponibles de Groq
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"

MODELS = {
    # Groq Models (solo los 2 disponibles)
    "groq-default": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "groq-llama": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    
    # OpenAI Models
    "openai-gpt4": {
        "provider": "openai",
        "model": "gpt-4",
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
    },
    "openai-gpt3.5": {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
    },
    
    # Anthropic Models
    "anthropic-claude": {
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "api_key": ANTHROPIC_API_KEY,
        "base_url": "https://api.anthropic.com",
    },
    
    # Local API Models (Ollama, LM Studio, etc.)
    "local-llama": {
        "provider": "local",
        "model": "llama2",
        "api_key": LOCAL_API_KEY or "local-key",
        "base_url": os.getenv("LOCAL_API_URL", "http://localhost:11434/v1"),
    },
    "local-mistral": {
        "provider": "local",
        "model": "mistral",
        "api_key": LOCAL_API_KEY or "local-key",
        "base_url": os.getenv("LOCAL_API_URL", "http://localhost:11434/v1"),
    },
}

# Default model
DEFAULT_MODEL = "groq-default"

# Security and Authentication
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "generar_una_clave_secreta_aqui")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SESSION_SECRET = os.getenv("SESSION_SECRET", "generar_una_clave_secreta_aqui")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "generar_una_clave_secreta_aqui")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "generar_una_clave_secreta_aqui")

# Database and Cache
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./afw.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_KEY = os.getenv("REDIS_KEY", "redis_default_key")

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8001))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS origins - Configuración por entorno
if ENVIRONMENT == "production":
    # Producción - solo dominios autorizados
    CORS_ORIGINS = [
        os.getenv("FRONTEND_URL", "https://afw.production.com"),
        "https://www.afw.production.com",
    ]
elif ENVIRONMENT == "staging":
    # Staging - dominios de staging
    CORS_ORIGINS = [
        "https://staging.afw.production.com",
        "https://afw-staging.vercel.app",
        "http://localhost:3000",  # Para desarrollo local
        "http://127.0.0.1:3000",
    ]
else:
    # Desarrollo - localhost y puertos comunes
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173",
    ]

# CORS settings adicionales para seguridad
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-language",
    "content-language",
    "content-type",
    "authorization",
    "x-requested-with",
    "x-api-key",
    "x-client-id"
]

# CORS max age para caché de preflight (en segundos)
CORS_MAX_AGE = 86400  # 24 horas
