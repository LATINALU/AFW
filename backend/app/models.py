"""
Modelos Pydantic para el API v0.8.0
"""
from pydantic import BaseModel, validator, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ModelType(str, Enum):
    DEEPSEEK = "deepseek"
    GROQ_LLAMA = "groq-llama"
    GROQ_MIXTRAL = "groq-mixtral"


class ApiConfig(BaseModel):
    """Configuración de API proporcionada por el usuario"""
    id: str
    name: str
    type: str
    apiKey: str
    baseUrl: Optional[str] = None
    models: List[str] = []
    isActive: bool = True


class ChatRequest(BaseModel):
    """Request para chat con validaciones de seguridad v0.8.0"""
    message: str = Field(..., min_length=1, max_length=10000, description="Mensaje del usuario")
    agents: List[str] = Field(..., min_items=1, max_items=5, description="Lista de agentes (máx 5)")
    model: str = Field(default="groq-default", description="Modelo a usar")
    context: Optional[str] = Field(None, max_length=5000, description="Contexto adicional")
    apiConfig: Optional[Dict[str, Any]] = Field(None, description="Configuración de API")
    
    @validator('message')
    def validate_message_content(cls, v):
        """Validar y sanitizar mensaje"""
        return validate_message_input(v)
    
    @validator('agents')
    def validate_agents_list(cls, v):
        """Validar lista de agentes"""
        return validate_agents_input(v)
    
    @validator('model')
    def validate_model_name(cls, v):
        """Validar nombre del modelo"""
        return validate_model_input(v)
    
    @validator('apiConfig')
    def validate_api_configuration(cls, v):
        """Validar configuración de API"""
        return validate_api_config_input(v)


class ChatResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    success: bool
    result: str
    agents_used: List[str]
    model_used: str
    error: Optional[str] = None
    processing_time: Optional[float] = None
    rate_limit_remaining: Optional[int] = None


class AgentInfo(BaseModel):
    name: str
    role: str
    level: int
    goal: str


class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: List[str]
    agents_count: int
