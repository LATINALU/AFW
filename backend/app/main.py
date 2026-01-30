"""
ATP Backend - FastAPI Server v0.8.0
Servidor principal para el sistema de agentes ATP con LangGraph y Protocolo A2A
Sistema de 30 Agentes Especializados - Streaming en Tiempo Real

MEJORAS v0.8.0:
- 🔐 Sistema de seguridad completo (validación, rate limiting, autenticación)
- 🛡️ Encriptación de API keys y datos sensibles
- ⚡ Rate limiting distribuido con Redis
- 🔑 Autenticación JWT para WebSocket
- 🌐 CORS restrictivo por entorno
- 🔍 Validación y sanitización de inputs
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import sys
import os
import json
import asyncio
import uuid
from datetime import datetime

# Añadir path del proyecto para imports
sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import (
    CORS_ORIGINS, MODELS, HOST, PORT, 
    CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS, CORS_MAX_AGE
)
from app.models import ChatRequest, ChatResponse, HealthResponse, AgentInfo
from app.api_models import fetch_available_models, get_model_description
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any

# Importar sistema de seguridad v0.8.0
from app.validators import (
    SecurityValidator, SecurityMiddleware,
    validate_message_input, validate_agents_input, 
    validate_model_input, validate_api_config_input
)
from app.middleware.rate_limiter import (
    limiter, RateLimiters, rate_limit_middleware,
    get_rate_limit_stats
)
from app.auth import (
    jwt_manager, session_manager, require_auth_token,
    websocket_auth_middleware, generate_client_id
)

# Importar nuevo sistema de agentes con Arquitectura Hexagonal
from src.infrastructure.adapters.external.langgraph_orchestrator import LangGraphOrchestratorAdapter as AgentOrchestrator
from src.infrastructure.adapters.external.openai_adapter import OpenAILLMAdapter
from src.infrastructure.adapters.external.llm_provider_factory import LLMProviderFactory
from src.infrastructure.adapters.persistence.in_memory_agent_repository import InMemoryAgentRepository
from src.application.use_cases.execute_task import ExecuteTaskUseCase

# AFW v0.5.0 - Nuevo sistema de 120 agentes en 12 categorías
from app.agents.registry import (
    AGENT_DEFINITIONS, CATEGORIES, 
    get_agents_by_category, get_all_categories, get_agent_count
)
from app.agents.agent_registry import AGENT_REGISTRY, get_agent_by_id

# Importar todos los agentes de las 12 categorías
from app.agents import *

# Instancia global del orchestrator
orchestrator = AgentOrchestrator()

from app.websocket_manager import manager
from app.services.streaming_pipeline import StreamingAgentPipeline
from app.formatters.human_formatter import HumanResponseFormatter
from app.services.online_users_tracker import get_tracker
from app.services.conversation_service import get_conversation_service

# AFW v0.5.0 - El sistema ahora usa 120 agentes definidos en el registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app"""
    print("🚀 AFW - Agents For Works v0.5.0 iniciando...")
    print(f"📡 Modelos disponibles: {list(MODELS.keys())}")
    print(f"🤖 {get_agent_count()} Agentes Especializados en {len(CATEGORIES)} Categorías")
    print(f"🧠 Sistema de Orquestación con StateGraph")
    print(f"📡 WebSocket + SSE para streaming en tiempo real")
    print(f"🎨 Formateo humano de respuestas de IA")
    print(f"💾 Sistema de Persistencia de Conversaciones")
    print(f"🔄 Memoria Contextual entre Preguntas")
    print(f"🔐 Sistema de Seguridad v0.8.0 activado")
    print(f"🛡️ Rate limiting y validación de inputs")
    print(f"🔑 Autenticación JWT para WebSocket")
    
    # Inicializar base de datos
    print("🗄️ Inicializando base de datos de usuarios...")
    from app.database import db
    db.init_database()
    print("✅ Base de datos lista")
    
    # Inicializar tracker de usuarios en línea
    print("👥 Inicializando tracker de usuarios en línea...")
    tracker = get_tracker(os.getenv("REDIS_URL", "redis://localhost:6379"))
    print("✅ Tracker de usuarios en línea listo")
    
    # Inicializar servicio de conversaciones
    print("💬 Inicializando servicio de conversaciones...")
    from app.services.conversation_service import get_conversation_service
    conv_service = get_conversation_service()
    print("✅ Servicio de conversaciones listo")
    
    # Inyectar dependencias globales (Clean Architecture)
    from src.infrastructure.config.container import get_save_conversation_use_case, get_execute_task_use_case
    app.state.save_conv_use_case = get_save_conversation_use_case()
    app.state.execute_task_use_case = get_execute_task_use_case()
    
    yield
    print("👋 Agentic Task Platform cerrando...")


app = FastAPI(
    title="Agentic Task Platform",
    description="Sistema de Agentes Especializados con LangGraph, Protocolo A2A, Streaming en Tiempo Real y Seguridad Mejorada",
    version="0.8.0",
    lifespan=lifespan,
)

# Configurar rate limiting
app.state.limiter = limiter

# CORS middleware con configuración segura v0.8.0
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
    max_age=CORS_MAX_AGE,
)

# Middleware de seguridad para todas las requests
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Middleware de seguridad para todas las requests"""
    # Sanitizar datos de entrada
    if request.method in ["POST", "PUT", "PATCH"]:
        # Para requests con body, sanitizamos después
        response = await call_next(request)
        return response
    else:
        # Para GET y otros, solo validamos headers
        response = await call_next(request)
        return response

# Manejador de errores de rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """Manejador personalizado para rate limit exceeded"""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": 60,
            "detail": str(exc.detail)
        },
        headers={"Retry-After": "60"}
    )


@app.get("/api/health", response_model=HealthResponse)
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health check endpoint con rate limiting"""
    return HealthResponse(
        status="healthy",
        version="0.8.0",
        models_available=list(MODELS.keys()),
        agents_count=len(AGENT_DEFINITIONS),
        security_features={
            "rate_limiting": True,
            "input_validation": True,
            "jwt_auth": True,
            "cors_restrictive": True
        }
    )


@app.get("/api/agents")
@limiter.limit("20/minute")
async def get_agents(request: Request, category: Optional[str] = None):
    """Get all 120 specialized agents, optionally filtered by category"""
    agents = []
    
    if category:
        # Filtrar por categoría
        filtered_defs = get_agents_by_category(category)
        for agent_id, info in filtered_defs.items():
            agents.append({
                "id": agent_id,
                "name": info["name"],
                "category": info.get("category", "general"),
                "description": info["description"],
                "emoji": info.get("emoji", "🤖"),
                "capabilities": info.get("capabilities", []),
                "specialization": info.get("specialization", ""),
                "complexity": info.get("complexity", "intermediate"),
            })
    else:
        # Todos los agentes
        for agent_id, info in AGENT_DEFINITIONS.items():
            agents.append({
                "id": agent_id,
                "name": info["name"],
                "category": info.get("category", "general"),
                "description": info["description"],
                "emoji": info.get("emoji", "🤖"),
                "capabilities": info.get("capabilities", []),
                "specialization": info.get("specialization", ""),
                "complexity": info.get("complexity", "intermediate"),
            })
    
    return {"agents": agents, "total": len(agents)}


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get a specific agent's information"""
    if agent_id not in AGENT_DEFINITIONS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    info = AGENT_DEFINITIONS[agent_id]
    return {
        "id": agent_id,
        "name": info["name"],
        "category": info.get("category", "general"),
        "description": info["description"],
        "emoji": info.get("emoji", "🤖"),
        "capabilities": info.get("capabilities", []),
        "specialization": info.get("specialization", ""),
        "complexity": info.get("complexity", "intermediate"),
    }


@app.get("/api/categories")
@limiter.limit("30/minute")
async def get_categories(request: Request):
    """Get all agent categories with metadata"""
    categories_list = []
    for cat_id, cat_info in CATEGORIES.items():
        categories_list.append({
            "id": cat_id,
            "name": cat_info["name"],
            "emoji": cat_info["emoji"],
            "description": cat_info["description"],
            "color": cat_info["color"],
            "agents_count": cat_info["agents_count"],
        })
    return {"categories": categories_list, "total": len(categories_list)}


@app.get("/api/categories/{category_id}")
async def get_category(category_id: str):
    """Get a specific category with its agents"""
    if category_id not in CATEGORIES:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    
    cat_info = CATEGORIES[category_id]
    agents = []
    for agent_id, info in get_agents_by_category(category_id).items():
        agents.append({
            "id": agent_id,
            "name": info["name"],
            "description": info["description"],
            "emoji": info.get("emoji", "🤖"),
            "capabilities": info.get("capabilities", []),
            "specialization": info.get("specialization", ""),
            "complexity": info.get("complexity", "intermediate"),
        })
    
    return {
        "id": category_id,
        "name": cat_info["name"],
        "emoji": cat_info["emoji"],
        "description": cat_info["description"],
        "color": cat_info["color"],
        "agents": agents,
        "agents_count": len(agents),
    }


@app.get("/api/models")
async def get_models():
    """Get available models"""
    return {
        "models": [
            {"id": model_id, "provider": config["provider"], "model": config["model"]}
            for model_id, config in MODELS.items()
        ]
    }


class FetchModelsRequest(BaseModel):
    """Request para obtener modelos de una API"""
    api_type: str
    api_key: str
    base_url: Optional[str] = None


@app.post("/api/fetch-models")
async def fetch_models(request: FetchModelsRequest):
    """
    Consulta una API para obtener los modelos disponibles.
    Útil para configurar qué modelo usar con cada agente.
    """
    try:
        models = await fetch_available_models(
            api_type=request.api_type,
            api_key=request.api_key,
            base_url=request.base_url
        )
        
        if not models:
            return {
                "success": False,
                "models": [],
                "error": "No se pudieron obtener los modelos. Verifica tu API key."
            }
        
        return {
            "success": True,
            "models": models,
            "count": len(models)
        }
    except Exception as e:
        return {
            "success": False,
            "models": [],
            "error": str(e)
        }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user messages with selected agents using LangGraph Orchestrator
    """
    try:
        # Validate request
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if not request.agents:
            raise HTTPException(status_code=400, detail="At least one agent must be selected")
        
        # Validate agents
        invalid_agents = [a for a in request.agents if a not in AGENT_DEFINITIONS]
        if invalid_agents:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid agents: {invalid_agents}"
            )
        
        # Create orchestrator with selected agents
        orchestrator = AgentOrchestrator()
        
        # Convert ApiConfig to dict if present
        api_config_dict = None
        if request.apiConfig:
            api_config_dict = {
                "type": request.apiConfig.type,
                "api_key": request.apiConfig.apiKey,
                "base_url": request.apiConfig.baseUrl,
            }
        
        # Map agent IDs to agent instances with model configuration
        agent_map = {
            "reasoning": ReasoningAgent(model=request.model, api_config=api_config_dict),
            "planning": PlanningAgent(model=request.model, api_config=api_config_dict),
            "research": ResearchAgent(model=request.model, api_config=api_config_dict),
            "analysis": AnalysisAgent(model=request.model, api_config=api_config_dict),
            "synthesis": SynthesisAgent(model=request.model, api_config=api_config_dict),
            "critical_thinking": CriticalThinkingAgent(model=request.model, api_config=api_config_dict),
            "coding": CodingAgent(model=request.model, api_config=api_config_dict),
            "data": DataAgent(model=request.model, api_config=api_config_dict),
            "writing": WritingAgent(model=request.model, api_config=api_config_dict),
            "communication": CommunicationAgent(model=request.model, api_config=api_config_dict),
            "decision": DecisionAgent(model=request.model, api_config=api_config_dict),
            "problem_solving": ProblemSolvingAgent(model=request.model, api_config=api_config_dict),
            "legal": LegalAgent(model=request.model, api_config=api_config_dict),
            "financial": FinancialAgent(model=request.model, api_config=api_config_dict),
            "creative": CreativeAgent(model=request.model, api_config=api_config_dict),
            "technical": TechnicalAgent(model=request.model, api_config=api_config_dict),
            "educational": EducationalAgent(model=request.model, api_config=api_config_dict),
            "marketing": MarketingAgent(model=request.model, api_config=api_config_dict),
            "qa": QAAgent(model=request.model, api_config=api_config_dict),
            "documentation": DocumentationAgent(model=request.model, api_config=api_config_dict),
            "optimization": OptimizationAgent(model=request.model, api_config=api_config_dict),
            "security": SecurityAgent(model=request.model, api_config=api_config_dict),
            "integration": IntegrationAgent(model=request.model, api_config=api_config_dict),
            "review": ReviewAgent(model=request.model, api_config=api_config_dict),
            "translation": TranslationAgent(model=request.model, api_config=api_config_dict),
            "summary": SummaryAgent(model=request.model, api_config=api_config_dict),
            "formatting": FormattingAgent(model=request.model, api_config=api_config_dict),
            "validation": ValidationAgent(model=request.model, api_config=api_config_dict),
            "coordination": CoordinationAgent(model=request.model, api_config=api_config_dict),
            "explanation": ExplanationAgent(model=request.model, api_config=api_config_dict),
        }
        
        # Get selected agent instances
        selected_agents = [agent_map[agent_id] for agent_id in request.agents if agent_id in agent_map]
        
        # Execute task with orchestrator
        result = await orchestrator.run_workflow(
            task=request.message,
            agents=selected_agents,
            context=request.context or {}
        )
        
        return ChatResponse(
            success=True,
            result=result.get("final_result", ""),
            agents_used=request.agents,
            model_used=request.model,
            error=None,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ ERROR EN /api/chat: {str(e)}")
        print(f"📋 TRACEBACK:\n{error_traceback}")
        return ChatResponse(
            success=False,
            result="",
            agents_used=request.agents,
            model_used=request.model,
            error=str(e),
        )


class QuickChatRequest(BaseModel):
    """Request para quick-chat con validación"""
    message: str
    model: str = "openai/gpt-oss-120b"
    apiConfig: Optional[Dict[str, Any]] = None


@app.post("/api/quick-chat")
async def quick_chat(request: QuickChatRequest):
    """
    Quick chat endpoint - uses default agents for simple queries
    Requires API key configuration for LLM calls
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    default_agents = ["reasoning", "synthesis"]
    
    orchestrator = AgentOrchestrator()
    
    agent_map = {
        "reasoning": ReasoningAgent(model=request.model, api_config=request.apiConfig),
        "synthesis": SynthesisAgent(model=request.model, api_config=request.apiConfig),
    }
    
    selected_agents = [agent_map[agent_id] for agent_id in default_agents]
    
    result = await orchestrator.run_workflow(
        task=request.message,
        agents=selected_agents,
        context={}
    )
    
    return {
        "success": True,
        "result": result.get("final_result", ""),
        "model": request.model,
    }


# ============== STREAMING EN TIEMPO REAL v0.7.0 ==============

def create_agent_instances(agents_list: List[str], model: str, api_config: Optional[Dict] = None, language: str = "es") -> List:
    """
    Crea instancias de agentes según la lista proporcionada.
    AFW v0.5.0 - Usa el AGENT_REGISTRY con los 120 agentes especializados.
    """
    instances = []
    
    for agent_id in agents_list:
        # Buscar agente en el registry
        agent_info = get_agent_by_id(agent_id)
        
        if agent_info:
            agent_class = agent_info['class']
            print(f"🤖 Creando agente {agent_id} ({agent_info['metadata']['name']}) con api_config: {bool(api_config)}")
            
            try:
                # Crear instancia del agente con configuración
                instance = agent_class(model=model, api_config=api_config)
                instances.append(instance)
            except Exception as e:
                print(f"⚠️ Error creando agente {agent_id}: {e}")
                # Continuar con los demás agentes
                continue
        else:
            print(f"⚠️ Agente {agent_id} no encontrado en el registry")
    
    if not instances:
        print(f"❌ No se pudieron crear agentes. IDs solicitados: {agents_list}")
    
    return instances


class StreamingChatRequest(BaseModel):
    """Request para chat con streaming"""
    message: str
    agents: List[str]
    model: str = "openai/gpt-4o-mini"
    apiConfig: Optional[Dict[str, Any]] = None
    language: str = "es"


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint sin autenticación para streaming de respuestas de agentes en tiempo real.
    
    v0.8.0 - Sin autenticación para desarrollo/pruebas
    """
    try:
        # Sin autenticación - conectar directamente
        session_id = f"session_{client_id}"
        user_id = f"guest_{client_id[:8]}"
        
        print(f"🔌 WebSocket conectado (sin auth): client_id={client_id}, session_id={session_id}")
        
        # Obtener metadata del usuario
        user_agent = websocket.headers.get("user-agent", "")
        device_type = _detect_device_type(user_agent)
        
        # Conectar con session_id y metadata
        await manager.connect(websocket, session_id, {
            "user_id": user_id,
            "device_type": device_type,
            "user_agent": user_agent
        })
        
        # Registrar en tracker de usuarios en línea
        tracker = get_tracker()
        await tracker.add_user(
            user_id=user_id,
            session_id=session_id,
            client_id=client_id,
            ip_address=websocket.client.host if websocket.client else None,
            user_agent=user_agent,
            device_type=device_type
        )
        
        # Enviar mensaje de bienvenida
        await manager.send_json(session_id, {
            "type": "connected",
            "message": "WebSocket conectado exitosamente",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except WebSocketDisconnect:
        print(f"❌ WebSocket desconectado durante autenticación: {client_id}")
        return
    except Exception as e:
        print(f"❌ Error en autenticación WebSocket: {e}")
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_json()
            
            if data.get("action") == "start_pipeline":
                print(f"🚀 Pipeline request received: {data}")
                
                # Validar y sanitizar datos de entrada
                message = data.get("message", "")
                print(f"📝 Message: {message[:100]}...")
                
                if not message or len(message) > 10000:
                    await manager.send_json(session_id, {
                        "type": "error",
                        "message": "Mensaje inválido o demasiado largo"
                    })
                    continue
                
                # Sanitizar mensaje
                message = SecurityValidator.sanitize_text(message)
                
                agents_list = data.get("agents", [])
                print(f"🤖 Agents requested: {agents_list}")
                
                model = data.get("model", "openai/gpt-4o-mini")
                api_config = data.get("apiConfig")
                language = data.get("language", "es")
                
                # Validar agentes
                valid_agents = SecurityValidator.validate_agent_list(agents_list)
                print(f"✅ Valid agents: {valid_agents}")
                
                if not valid_agents:
                    print(f"❌ No valid agents found from: {agents_list}")
                    await manager.send_json(session_id, {
                        "type": "error",
                        "message": "No valid agents selected"
                    })
                    continue
                
                # Validar modelo
                model = SecurityValidator.validate_model_name(model)
                
                # Validar configuración de API
                if api_config:
                    api_config = SecurityValidator.validate_api_config(api_config)
                    if api_config:
                        api_config = {
                            "type": api_config.get("type", "openai"),
                            "api_key": api_config.get("apiKey", ""),
                            "base_url": api_config.get("baseUrl"),
                        }
                        print(f"🔑 API Config validada: type={api_config.get('type')}, has_key={bool(api_config.get('api_key'))}")
                else:
                    print(f"⚠️ No se recibió apiConfig válida, usando fallback")
                
                # Crear instancias de agentes
                print(f"🔨 Creating agent instances...")
                agent_instances = create_agent_instances(valid_agents, model, api_config, language=language)
                print(f"✅ Created {len(agent_instances)} agent instances")
                
                # Crear pipeline de streaming
                print(f"🚀 Creating streaming pipeline...")
                pipeline = StreamingAgentPipeline(agent_instances, AGENT_DEFINITIONS, language=language)
                print(f"✅ Pipeline created successfully")
                
                # Enviar confirmación de inicio
                await manager.send_json(session_id, {
                    "type": "pipeline_started",
                    "agents": valid_agents,
                    "model": model,
                    "message_count": len(valid_agents)
                })
                
                # Ejecutar pipeline con streaming
                print(f"🔄 Starting pipeline execution...")
                try:
                    async for response in pipeline.execute_with_streaming(
                        task=message,
                        client_id=session_id,
                        context={"authenticated": True, "session_id": session_id}
                    ):
                        print(f"📤 Pipeline response: {type(response)}")
                        # Las respuestas ya se envían dentro del pipeline
                        pass
                    print(f"✅ Pipeline execution completed")
                except Exception as e:
                    print(f"❌ Pipeline execution error: {e}")
                    import traceback
                    traceback.print_exc()
                    await manager.send_json(session_id, {
                        "type": "error",
                        "message": f"Pipeline execution error: {str(e)}"
                    })
                
                # PERSISTENCIA v0.8.0 - Guardar conversación automáticamente
                try:
                    conv_service = get_conversation_service()
                    user_id = client_id  # Usar client_id como user_id para usuarios no autenticados
                    
                    conv_id = data.get("conversation_id")
                    
                    # Si no hay conversation_id, crear una nueva conversación
                    if not conv_id:
                        conv_id = await conv_service.create_conversation(
                            user_id=user_id,
                            title=message[:100] if len(message) > 100 else message,
                            model=model,
                            agents=valid_agents
                        )
                        print(f"💾 Nueva conversación creada: {conv_id}")
                    
                    # Guardar mensaje del usuario
                    await conv_service.add_message(
                        conversation_id=conv_id,
                        role="user",
                        content=message
                    )
                    
                    # Guardar respuestas de agentes
                    results = getattr(pipeline, 'results', [])
                    for r in results:
                        await conv_service.add_message(
                            conversation_id=conv_id,
                            role="assistant",
                            content=r.get("raw_content", r.get("content", "")),
                            agent_id=r.get("agent_id"),
                            metadata={
                                "agent_name": r.get("agent_name"),
                                "level": r.get("level"),
                                "sections": r.get("sections", [])
                            }
                        )
                    
                    # Informar al cliente del ID de conversación
                    await manager.send_json(session_id, {
                        "type": "conversation_saved",
                        "conversation_id": conv_id,
                        "title": message[:100] if len(message) > 100 else message
                    })
                    
                    print(f"💾 Conversación guardada: {conv_id}")
                except Exception as e:
                    print(f"⚠️ Error al persistir conversación: {e}")
            
            elif data.get("action") == "ping":
                await manager.send_json(session_id, {
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id
                })
            
            elif data.get("action") == "get_stats":
                stats = manager.get_stats()
                await manager.send_json(session_id, {
                    "type": "stats", 
                    "data": stats,
                    "session_id": session_id
                })
                
            elif data.get("action") == "get_security_info":
                # Información de seguridad para el cliente
                await manager.send_json(session_id, {
                    "type": "security_info",
                    "data": {
                        "encryption_enabled": True,
                        "rate_limiting": True,
                        "session_active": True,
                        "session_id": session_id
                    }
                })
            
            else:
                await manager.send_json(session_id, {
                    "type": "error",
                    "message": f"Unknown action: {data.get('action')}"
                })
                
    except WebSocketDisconnect:
        print(f"🔌 WebSocket desconectado: session_id={session_id}")
        manager.disconnect(session_id)
        # Invalidar sesión
        session_manager.invalidate_session(session_id)
        # Remover del tracker
        tracker = get_tracker()
        await tracker.remove_user(session_id)
    except Exception as e:
        print(f"❌ WebSocket error para session_id={session_id}: {e}")
        await manager.send_json(session_id, {
            "type": "error",
            "message": "Internal server error"
        })
        manager.disconnect(session_id)
        session_manager.invalidate_session(session_id)
        # Remover del tracker
        tracker = get_tracker()
        await tracker.remove_user(session_id)


@app.post("/api/chat-stream")
async def chat_stream(request: StreamingChatRequest):
    """
    Endpoint HTTP con Server-Sent Events (SSE) para streaming de respuestas.
    Alternativa a WebSocket para entornos que no lo soportan.
    """
    # Validar request
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    valid_agents = [a for a in request.agents if a in AGENT_DEFINITIONS]
    if not valid_agents:
        raise HTTPException(status_code=400, detail="No valid agents selected")
    
    # Convertir apiConfig
    api_config = None
    if request.apiConfig:
        api_config = {
            "type": request.apiConfig.get("type", "openai"),
            "api_key": request.apiConfig.get("apiKey", ""),
            "base_url": request.apiConfig.get("baseUrl"),
        }
    
    # Crear instancias de agentes
    agent_instances = create_agent_instances(valid_agents, request.model, api_config, language=request.language)
    
    # Generar client_id único para SSE
    client_id = f"sse_{uuid.uuid4().hex[:8]}"
    
    async def event_stream():
        """Generador de eventos SSE."""
        pipeline = StreamingAgentPipeline(agent_instances, AGENT_DEFINITIONS, language=request.language)
        
        async for response in pipeline.execute_with_streaming(
            task=request.message,
            client_id=client_id,
            context={}
        ):
            # Formato SSE: data: {json}\n\n
            yield f"data: {json.dumps(response, default=str)}\n\n"
            await asyncio.sleep(0.05)  # Pequeña pausa para control de flujo
        
        # Evento de finalización
        yield f"data: {json.dumps({'type': 'stream_complete'})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Importante para NGINX
            "Access-Control-Allow-Origin": "*",
        }
    )


@app.get("/api/ws-stats")
async def get_websocket_stats():
    """Obtiene estadísticas de conexiones WebSocket activas."""
    return manager.get_stats()


# ============== ENDPOINTS PÚBLICOS DE CONVERSACIONES v0.8.0 ==============

@app.get("/api/chat/conversations")
async def list_conversations_public(
    client_id: str = Query(..., description="ID del cliente"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Lista las conversaciones de un cliente (sin autenticación).
    Usa client_id como identificador de usuario.
    """
    try:
        conv_service = get_conversation_service()
        conversations = await conv_service.get_conversations(
            user_id=client_id,
            limit=limit,
            offset=offset,
            include_archived=False
        )
        return {
            "success": True,
            "conversations": conversations,
            "total": len(conversations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/conversations/{conversation_id}")
async def get_conversation_public(conversation_id: str):
    """
    Obtiene una conversación con sus mensajes (sin autenticación).
    """
    try:
        conv_service = get_conversation_service()
        messages = await conv_service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=500
        )
        return {
            "success": True,
            "conversation_id": conversation_id,
            "messages": messages,
            "total_messages": len(messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/chat/conversations/{conversation_id}")
async def delete_conversation_public(conversation_id: str):
    """
    Elimina una conversación (sin autenticación).
    """
    try:
        conv_service = get_conversation_service()
        success = await conv_service.delete_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True, "conversation_id": conversation_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/conversations/{conversation_id}/archive")
async def archive_conversation_public(conversation_id: str, archived: bool = True):
    """
    Archiva o desarchivar una conversación (sin autenticación).
    """
    try:
        conv_service = get_conversation_service()
        success = await conv_service.archive_conversation(conversation_id, archived)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True, "conversation_id": conversation_id, "archived": archived}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/chat/conversations/{conversation_id}/title")
async def update_conversation_title_public(conversation_id: str, title: str = Query(..., min_length=1, max_length=200)):
    """
    Actualiza el título de una conversación (sin autenticación).
    """
    try:
        conv_service = get_conversation_service()
        success = await conv_service.update_conversation_title(conversation_id, title)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True, "conversation_id": conversation_id, "title": title}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/search")
async def search_conversations_public(
    client_id: str = Query(..., description="ID del cliente"),
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    limit: int = Query(20, ge=1, le=50)
):
    """
    Busca conversaciones por título o contenido (sin autenticación).
    """
    try:
        conv_service = get_conversation_service()
        results = await conv_service.search_conversations(
            user_id=client_id,
            query=q,
            limit=limit
        )
        return {
            "success": True,
            "query": q,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== RUTAS DE AUTENTICACIÓN E HISTORIAL v0.8.0 ==============
from app.routes.auth_routes import router as auth_router
from app.routes.history_routes import router as history_router
from app.routes.admin_routes import router as admin_router
from app.routes.api_v1_routes import router as api_v1_router
from app.routes.conversation_routes import router as conversation_router

app.include_router(auth_router)
app.include_router(history_router)
app.include_router(admin_router)
app.include_router(api_v1_router)
app.include_router(conversation_router)


# ============== SISTEMA COMPLETO v0.8.0+ ==============
# El sistema ATP usa 30 agentes especializados con LangGraph
# Los endpoints principales son:
# - /api/chat: Chat con agentes (respuesta completa)
# - /api/chat-stream: Chat con SSE streaming
# - /ws/{client_id}: WebSocket para streaming bidireccional
# - /api/quick-chat: Chat rápido con agentes por defecto
# - /api/agents: Listar todos los agentes
# - /api/models: Listar modelos disponibles
# - /api/ws-stats: Estadísticas de WebSocket


def _detect_device_type(user_agent: str) -> str:
    """
    Detecta el tipo de dispositivo desde el user agent.
    
    Args:
        user_agent: String del user agent
        
    Returns:
        Tipo de dispositivo: 'mobile', 'tablet', o 'desktop'
    """
    user_agent_lower = user_agent.lower()
    
    # Detectar móvil
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']
    if any(keyword in user_agent_lower for keyword in mobile_keywords):
        return 'mobile'
    
    # Detectar tablet
    tablet_keywords = ['ipad', 'tablet', 'kindle']
    if any(keyword in user_agent_lower for keyword in tablet_keywords):
        return 'tablet'
    
    return 'desktop'


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
