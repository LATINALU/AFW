"""
ATP v0.8.0+ - History Routes
============================
Rutas para la gestión del historial de conversaciones
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.database import db
from app.auth import jwt_manager

router = APIRouter(prefix="/api/history", tags=["History"])

class ConversationSummary(BaseModel):
    conversation_id: str
    title: str
    created_at: str
    updated_at: str
    model: str
    agents: List[str]

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ConversationDetail(BaseModel):
    conversation_id: str
    title: str
    messages: List[Dict[str, Any]]
    model: str
    agents: List[str]
    created_at: str
    updated_at: str

@router.get("", response_model=List[ConversationSummary])
async def get_history(authorization: str = Header(...)):
    """Obtener historial de conversaciones del usuario"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        conversations = db.get_user_conversations(user_id)
        return conversations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: str, authorization: str = Header(...)):
    """Obtener detalle de una conversación específica"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        # Consultar DB
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE conversation_id = ? AND user_id = ?
        """, (conversation_id, user_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        
        import json
        conv = dict(row)
        return ConversationDetail(
            conversation_id=conv["conversation_id"],
            title=conv["title"],
            messages=json.loads(conv["messages"]) if conv["messages"] else [],
            model=conv["model"] or "",
            agents=json.loads(conv["agents"]) if conv["agents"] else [],
            created_at=conv["created_at"],
            updated_at=conv["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, authorization: str = Header(...)):
    """Eliminar una conversación"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE conversation_id = ? AND user_id = ?", 
                      (conversation_id, user_id))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Conversación eliminada"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{conversation_id}/title")
async def update_title(conversation_id: str, title_data: Dict[str, str], authorization: str = Header(...)):
    """Actualizar el título de una conversación"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        new_title = title_data.get("title")
        if not new_title:
            raise HTTPException(status_code=400, detail="Título requerido")
            
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE conversation_id = ? AND user_id = ?
        """, (new_title, conversation_id, user_id))
        conn.commit()
        conn.close()
        
        return {"success": True, "title": new_title}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync")
async def sync_history(conversations: List[Dict[str, Any]], authorization: str = Header(...)):
    """Sincronizar historial local con el servidor"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        count = 0
        for conv in conversations:
            # Mapeo de campos (Frontend -> Backend)
            conv_id = conv.get("id") or conv.get("conversation_id")
            if not conv_id:
                continue
                
            db.save_conversation(
                user_id=user_id,
                conversation_id=conv_id,
                title=conv.get("title", "Sin título"),
                messages=conv.get("messages", []),
                model=conv.get("model", "llama-3.3-70b-versatile"),
                agents=conv.get("agents", [])
            )
            count += 1
            
        return {"success": True, "synced_count": count}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
