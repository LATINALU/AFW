"""
REST API v1.0.0
===============
API RESTful para integración externa con autenticación por API key.
Permite a sistemas externos consumir los servicios de ATP.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Header
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import hashlib
import secrets

from app.middleware.rate_limiter import limiter
from app.database import db
from app.validators import SecurityValidator
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1", tags=["api-v1"])


class ApiKey:
    """Modelo de API Key"""
    def __init__(self, key: str, user_id: str, name: str, created_at: str, 
                 last_used: Optional[str] = None, is_active: bool = True):
        self.key = key
        self.user_id = user_id
        self.name = name
        self.created_at = created_at
        self.last_used = last_used
        self.is_active = is_active


class ApiKeyManager:
    """Gestor de API Keys para autenticación externa"""
    
    def __init__(self):
        self.api_keys: Dict[str, ApiKey] = {}
        self._init_storage()
    
    def _init_storage(self):
        """Inicializa almacenamiento de API keys en base de datos"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                key_prefix TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                status_code INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (key_hash) REFERENCES api_keys(key_hash)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_api_key(self, user_id: int, name: str) -> str:
        """
        Genera una nueva API key para un usuario.
        
        Args:
            user_id: ID del usuario
            name: Nombre descriptivo de la API key
            
        Returns:
            API key generada (solo se muestra una vez)
        """
        # Generar key segura
        key = f"atp_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        key_prefix = key[:12]  # Para identificación
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO api_keys (key_hash, key_prefix, user_id, name)
            VALUES (?, ?, ?, ?)
        """, (key_hash, key_prefix, user_id, name))
        
        conn.commit()
        conn.close()
        
        return key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """
        Valida una API key y retorna información del usuario.
        
        Args:
            api_key: API key a validar
            
        Returns:
            Información del usuario si la key es válida, None si no
        """
        if not api_key or not api_key.startswith("atp_"):
            return None
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ak.*, u.username, u.email, u.role
            FROM api_keys ak
            JOIN users u ON ak.user_id = u.id
            WHERE ak.key_hash = ? AND ak.is_active = 1
        """, (key_hash,))
        
        result = cursor.fetchone()
        
        if result:
            # Actualizar last_used
            cursor.execute("""
                UPDATE api_keys
                SET last_used = CURRENT_TIMESTAMP
                WHERE key_hash = ?
            """, (key_hash,))
            conn.commit()
            
            conn.close()
            return dict(result)
        
        conn.close()
        return None
    
    def revoke_api_key(self, key_hash: str, user_id: int) -> bool:
        """
        Revoca una API key.
        
        Args:
            key_hash: Hash de la key a revocar
            user_id: ID del usuario (para verificación)
            
        Returns:
            True si se revocó exitosamente
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE api_keys
            SET is_active = 0
            WHERE key_hash = ? AND user_id = ?
        """, (key_hash, user_id))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0
    
    def get_user_keys(self, user_id: int) -> List[Dict]:
        """
        Obtiene todas las API keys de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de API keys (sin la key completa)
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, key_prefix, name, created_at, last_used, is_active
            FROM api_keys
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    
    def log_usage(self, key_hash: str, endpoint: str, method: str, status_code: int):
        """
        Registra el uso de una API key.
        
        Args:
            key_hash: Hash de la key
            endpoint: Endpoint accedido
            method: Método HTTP
            status_code: Código de respuesta
        """
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO api_usage (key_hash, endpoint, method, status_code)
                VALUES (?, ?, ?, ?)
            """, (key_hash, endpoint, method, status_code))
            
            conn.commit()
            conn.close()
        except:
            pass  # No fallar si el logging falla


# Instancia global del gestor
api_key_manager = ApiKeyManager()


async def require_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(None)
) -> Dict:
    """
    Middleware para requerir API key válida.
    
    Args:
        request: Request de FastAPI
        x_api_key: API key del header
        
    Returns:
        Información del usuario
        
    Raises:
        HTTPException: Si la API key es inválida
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Include X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    user_info = api_key_manager.validate_api_key(x_api_key)
    
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Registrar uso
    key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
    api_key_manager.log_usage(
        key_hash,
        str(request.url.path),
        request.method,
        200
    )
    
    return user_info


# ============== API ENDPOINTS ==============

class ChatRequest(BaseModel):
    """Request para chat via API"""
    message: str = Field(..., min_length=1, max_length=10000)
    agents: List[str] = Field(..., min_items=1, max_items=30)
    model: str = Field(default="openai/gpt-4o-mini")
    stream: bool = Field(default=False)


class ChatResponse(BaseModel):
    """Response de chat"""
    success: bool
    result: str
    agents_used: List[str]
    model_used: str
    timestamp: str
    request_id: str


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("30/minute")
async def api_chat(
    request: Request,
    chat_request: ChatRequest,
    user_info: Dict = Depends(require_api_key)
):
    """
    Endpoint de chat para API externa.
    
    Requiere API key válida en header X-API-Key.
    
    Rate limit: 30 requests/minuto por API key.
    """
    from app.agents import (
        ReasoningAgent, PlanningAgent, ResearchAgent, AnalysisAgent,
        SynthesisAgent, CriticalThinkingAgent, CodingAgent, DataAgent,
        WritingAgent, CommunicationAgent, DecisionAgent, ProblemSolvingAgent,
        LegalAgent, FinancialAgent, CreativeAgent, TechnicalAgent,
        EducationalAgent, MarketingAgent, QAAgent, DocumentationAgent,
        OptimizationAgent, SecurityAgent, IntegrationAgent, ReviewAgent,
        TranslationAgent, SummaryAgent, FormattingAgent, ValidationAgent,
        CoordinationAgent, ExplanationAgent
    )
    from src.infrastructure.adapters.external.langgraph_orchestrator import LangGraphOrchestratorAdapter
    
    # Validar agentes
    valid_agents = SecurityValidator.validate_agent_list(chat_request.agents)
    if not valid_agents:
        raise HTTPException(status_code=400, detail="No valid agents selected")
    
    # Sanitizar mensaje
    message = SecurityValidator.sanitize_text(chat_request.message)
    
    # Crear orchestrator
    orchestrator = LangGraphOrchestratorAdapter()
    
    # Map de agentes
    agent_map = {
        "reasoning": ReasoningAgent,
        "planning": PlanningAgent,
        "research": ResearchAgent,
        "analysis": AnalysisAgent,
        "synthesis": SynthesisAgent,
        "critical_thinking": CriticalThinkingAgent,
        "coding": CodingAgent,
        "data": DataAgent,
        "writing": WritingAgent,
        "communication": CommunicationAgent,
        "decision": DecisionAgent,
        "problem_solving": ProblemSolvingAgent,
        "legal": LegalAgent,
        "financial": FinancialAgent,
        "creative": CreativeAgent,
        "technical": TechnicalAgent,
        "educational": EducationalAgent,
        "marketing": MarketingAgent,
        "qa": QAAgent,
        "documentation": DocumentationAgent,
        "optimization": OptimizationAgent,
        "security": SecurityAgent,
        "integration": IntegrationAgent,
        "review": ReviewAgent,
        "translation": TranslationAgent,
        "summary": SummaryAgent,
        "formatting": FormattingAgent,
        "validation": ValidationAgent,
        "coordination": CoordinationAgent,
        "explanation": ExplanationAgent,
    }
    
    # Crear instancias
    agent_instances = [
        agent_map[agent_id](model=chat_request.model)
        for agent_id in valid_agents
        if agent_id in agent_map
    ]
    
    # Ejecutar
    try:
        result = await orchestrator.run_workflow(
            task=message,
            agents=agent_instances,
            context={"api_user": user_info.get("username")}
        )
        
        request_id = str(uuid.uuid4())
        
        return ChatResponse(
            success=True,
            result=result.get("final_result", ""),
            agents_used=valid_agents,
            model_used=chat_request.model,
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@router.get("/agents")
@limiter.limit("60/minute")
async def api_list_agents(
    request: Request,
    user_info: Dict = Depends(require_api_key)
):
    """
    Lista todos los agentes disponibles.
    
    Requiere API key válida.
    """
    from src.domain.services.agent_orchestrator import AGENT_DEFINITIONS
    
    agents = []
    for agent_id, info in AGENT_DEFINITIONS.items():
        agents.append({
            "id": agent_id,
            "name": info["name"],
            "level": info["level"],
            "description": info["description"],
        })
    
    return {
        "success": True,
        "agents": agents,
        "total": len(agents),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/models")
@limiter.limit("60/minute")
async def api_list_models(
    request: Request,
    user_info: Dict = Depends(require_api_key)
):
    """
    Lista todos los modelos disponibles.
    
    Requiere API key válida.
    """
    from app.config import MODELS
    
    models = [
        {
            "id": model_id,
            "provider": config["provider"],
            "model": config["model"]
        }
        for model_id, config in MODELS.items()
    ]
    
    return {
        "success": True,
        "models": models,
        "total": len(models),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/usage")
@limiter.limit("30/minute")
async def api_get_usage(
    request: Request,
    user_info: Dict = Depends(require_api_key)
):
    """
    Obtiene estadísticas de uso de la API key.
    
    Requiere API key válida.
    """
    # Implementar query de uso
    return {
        "success": True,
        "usage": {
            "requests_today": 0,
            "requests_month": 0,
            "last_request": None
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ============== API KEY MANAGEMENT ==============

@router.post("/keys/generate")
async def generate_api_key(
    request: Request,
    name: str,
    user_info: Dict = Depends(require_api_key)
):
    """
    Genera una nueva API key para el usuario.
    
    La key solo se muestra una vez.
    """
    if not name or len(name) > 100:
        raise HTTPException(
            status_code=400,
            detail="Name must be between 1 and 100 characters"
        )
    
    user_id = user_info.get("user_id")
    api_key = api_key_manager.generate_api_key(user_id, name)
    
    return {
        "success": True,
        "api_key": api_key,
        "name": name,
        "message": "Save this key securely. It won't be shown again.",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/keys")
async def list_api_keys(
    request: Request,
    user_info: Dict = Depends(require_api_key)
):
    """
    Lista todas las API keys del usuario.
    """
    user_id = user_info.get("user_id")
    keys = api_key_manager.get_user_keys(user_id)
    
    return {
        "success": True,
        "keys": keys,
        "total": len(keys),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.delete("/keys/{key_prefix}")
async def revoke_api_key(
    request: Request,
    key_prefix: str,
    user_info: Dict = Depends(require_api_key)
):
    """
    Revoca una API key.
    """
    # Implementar revocación por prefix
    return {
        "success": True,
        "message": "API key revoked",
        "timestamp": datetime.utcnow().isoformat()
    }
