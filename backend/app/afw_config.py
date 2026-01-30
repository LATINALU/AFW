"""
AFW v0.5.0 - Agents For Works Configuration
Configuración principal del sistema de 120 agentes especializados en 12 categorías
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# AFW CORE CONFIGURATION
# ============================================================================

# Version
AFW_VERSION = "0.5.0"
AFW_NAME = "Agents For Works"
AFW_TAGLINE = "Potencia tu trabajo con 120 agentes especializados"

# Agent Limits - UPDATED FOR AFW v0.5.0
MAX_AGENTS_PER_TASK = 10  # Increased from 5 to 10
TOTAL_AGENTS = 120        # Total available agents (12 categories x 10 agents)
MIN_AGENTS_PER_TASK = 1   # Minimum agents required

# Agent Categories
AGENT_CATEGORIES = [
    "software_development",
    "marketing",
    "finance",
    "legal",
    "human_resources",
    "sales",
    "operations",
    "education",
    "creative",
    "project_management",
    "mercadolibre",
    "youtube"
]

CATEGORY_DISPLAY_NAMES = {
    "software_development": "💻 Desarrollo de Software",
    "marketing": "📢 Marketing Digital",
    "finance": "💰 Finanzas y Contabilidad",
    "legal": "⚖️ Legal y Compliance",
    "human_resources": "👥 Recursos Humanos",
    "sales": "💼 Ventas y Comercial",
    "operations": "⚙️ Operaciones y Logística",
    "education": "📚 Educación y Capacitación",
    "creative": "🎨 Creatividad y Diseño",
    "project_management": "📋 Gestión de Proyectos",
    "mercadolibre": "🛒 Mercado Libre",
    "youtube": "▶️ YouTube"
}

# Workflow Configuration
MAX_WORKFLOWS = 50
WORKFLOW_CATEGORIES = [
    "software_development",
    "marketing",
    "finance",
    "legal",
    "human_resources",
    "sales",
    "operations",
    "education",
    "creative",
    "project_management",
    "mercadolibre",
    "youtube"
]

# ============================================================================
# API PROVIDERS CONFIGURATION
# ============================================================================

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY")

# Default Model
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

MODELS = {
    "groq-default": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "groq-fast": {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "openai-gpt4": {
        "provider": "openai",
        "model": "gpt-4-turbo-preview",
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
    },
    "openai-gpt3.5": {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
    },
    "anthropic-claude": {
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "api_key": ANTHROPIC_API_KEY,
        "base_url": "https://api.anthropic.com",
    },
    "local-ollama": {
        "provider": "local",
        "model": os.getenv("LOCAL_MODEL", "llama2"),
        "api_key": LOCAL_API_KEY or "local-key",
        "base_url": os.getenv("LOCAL_API_URL", "http://localhost:11434/v1"),
    },
}

DEFAULT_MODEL = "groq-default"

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "afw_secret_key_v050_change_me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SESSION_SECRET = os.getenv("SESSION_SECRET", "afw_session_secret_v050")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "afw_encryption_key_v050")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "afw_api_secret_v050")

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./afw.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_KEY = os.getenv("REDIS_KEY", "afw_redis_key_v050")

# ============================================================================
# SERVER CONFIGURATION
# ============================================================================

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8001))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

if ENVIRONMENT == "production":
    CORS_ORIGINS = [
        os.getenv("FRONTEND_URL", "https://afw.production.com"),
        "https://www.afw.production.com",
    ]
elif ENVIRONMENT == "staging":
    CORS_ORIGINS = [
        "https://staging.afw.production.com",
        "https://afw-staging.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
else:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

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
CORS_MAX_AGE = 86400

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    "streaming_enabled": True,
    "memory_enabled": True,
    "multi_provider": True,
    "workflows_enabled": True,
    "max_agents_10": True,  # New feature: 10 agents per task
    "100_agents": True,      # New feature: 100 total agents
}
