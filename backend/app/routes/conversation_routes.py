"""
Conversation Routes v1.0.0
==========================
Endpoints para gestión de conversaciones y respuestas guardadas.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.services.conversation_service import get_conversation_service
from app.middleware.rate_limiter import limiter
from app.auth import require_auth_token

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


# ============== MODELS ==============

class CreateConversationRequest(BaseModel):
    """Request para crear conversación"""
    title: str = Field(..., min_length=1, max_length=200)
    model: Optional[str] = None
    agents: Optional[List[str]] = None


class AddMessageRequest(BaseModel):
    """Request para agregar mensaje"""
    conversation_id: str
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)
    agent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SaveResponseRequest(BaseModel):
    """Request para guardar respuesta"""
    agent_id: str
    agent_name: str
    content: str = Field(..., min_length=1)
    title: Optional[str] = None
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class UpdateTitleRequest(BaseModel):
    """Request para actualizar título"""
    title: str = Field(..., min_length=1, max_length=200)


# ============== CONVERSATION ENDPOINTS ==============

@router.post("/create")
@limiter.limit("30/minute")
async def create_conversation(
    request: Request,
    data: CreateConversationRequest,
    token_data: dict = Depends(require_auth_token)
):
    """
    Crea una nueva conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    user_id = token_data.get("user_id", "guest")
    
    try:
        conversation_id = await service.create_conversation(
            user_id=str(user_id),
            title=data.title,
            model=data.model,
            agents=data.agents
        )
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "title": data.title,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message")
@limiter.limit("60/minute")
async def add_message(
    request: Request,
    data: AddMessageRequest,
    token_data: dict = Depends(require_auth_token)
):
    """
    Agrega un mensaje a una conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        message_id = await service.add_message(
            conversation_id=data.conversation_id,
            role=data.role,
            content=data.content,
            agent_id=data.agent_id,
            metadata=data.metadata
        )
        
        return {
            "success": True,
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
@limiter.limit("30/minute")
async def list_conversations(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    include_archived: bool = False,
    token_data: dict = Depends(require_auth_token)
):
    """
    Lista las conversaciones del usuario.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    user_id = token_data.get("user_id", "guest")
    
    try:
        conversations = await service.get_conversations(
            user_id=str(user_id),
            limit=min(limit, 100),
            offset=offset,
            include_archived=include_archived
        )
        
        return {
            "success": True,
            "conversations": conversations,
            "total": len(conversations),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}")
@limiter.limit("60/minute")
async def get_conversation(
    request: Request,
    conversation_id: str,
    token_data: dict = Depends(require_auth_token)
):
    """
    Obtiene una conversación con sus mensajes.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        messages = await service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=1000
        )
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "messages": messages,
            "total_messages": len(messages),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{conversation_id}/title")
@limiter.limit("20/minute")
async def update_title(
    request: Request,
    conversation_id: str,
    data: UpdateTitleRequest,
    token_data: dict = Depends(require_auth_token)
):
    """
    Actualiza el título de una conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        success = await service.update_conversation_title(
            conversation_id=conversation_id,
            title=data.title
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "title": data.title,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conversation_id}")
@limiter.limit("20/minute")
async def delete_conversation(
    request: Request,
    conversation_id: str,
    token_data: dict = Depends(require_auth_token)
):
    """
    Elimina una conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        success = await service.delete_conversation(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/archive")
@limiter.limit("20/minute")
async def archive_conversation(
    request: Request,
    conversation_id: str,
    archived: bool = True,
    token_data: dict = Depends(require_auth_token)
):
    """
    Archiva o desarchivar una conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        success = await service.archive_conversation(conversation_id, archived)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "archived": archived,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/pin")
@limiter.limit("20/minute")
async def pin_conversation(
    request: Request,
    conversation_id: str,
    pinned: bool = True,
    token_data: dict = Depends(require_auth_token)
):
    """
    Fija o desfija una conversación.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        success = await service.pin_conversation(conversation_id, pinned)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "pinned": pinned,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
@limiter.limit("30/minute")
async def search_conversations(
    request: Request,
    q: str,
    limit: int = 20,
    token_data: dict = Depends(require_auth_token)
):
    """
    Busca conversaciones por título o contenido.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    user_id = token_data.get("user_id", "guest")
    
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    try:
        results = await service.search_conversations(
            user_id=str(user_id),
            query=q,
            limit=min(limit, 50)
        )
        
        return {
            "success": True,
            "query": q,
            "results": results,
            "total": len(results),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== SAVED RESPONSES ENDPOINTS ==============

@router.post("/responses/save")
@limiter.limit("30/minute")
async def save_response(
    request: Request,
    data: SaveResponseRequest,
    token_data: dict = Depends(require_auth_token)
):
    """
    Guarda una respuesta individual de un agente.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    user_id = token_data.get("user_id", "guest")
    
    try:
        response_id = await service.save_response(
            user_id=str(user_id),
            agent_id=data.agent_id,
            agent_name=data.agent_name,
            content=data.content,
            title=data.title,
            conversation_id=data.conversation_id,
            message_id=data.message_id,
            tags=data.tags,
            category=data.category
        )
        
        return {
            "success": True,
            "response_id": response_id,
            "message": "Response saved successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/responses/list")
@limiter.limit("30/minute")
async def list_saved_responses(
    request: Request,
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    token_data: dict = Depends(require_auth_token)
):
    """
    Lista las respuestas guardadas del usuario.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    user_id = token_data.get("user_id", "guest")
    
    try:
        responses = await service.get_saved_responses(
            user_id=str(user_id),
            category=category,
            limit=min(limit, 100),
            offset=offset
        )
        
        return {
            "success": True,
            "responses": responses,
            "total": len(responses),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/responses/{response_id}")
@limiter.limit("20/minute")
async def delete_saved_response(
    request: Request,
    response_id: str,
    token_data: dict = Depends(require_auth_token)
):
    """
    Elimina una respuesta guardada.
    
    Requiere autenticación.
    """
    service = get_conversation_service()
    
    try:
        success = await service.delete_saved_response(response_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Response not found")
        
        return {
            "success": True,
            "response_id": response_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
