from fastapi import APIRouter, Header, HTTPException, Depends
from typing import List
from src.application.use_cases.get_chat_history import GetChatHistoryUseCase
from src.infrastructure.config.container import get_history_use_case
from app.auth import jwt_manager

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("")
async def get_history(
    authorization: str = Header(...),
    use_case: GetChatHistoryUseCase = Depends(get_history_use_case)
):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # El controlador solo llama al caso de uso
        conversations = use_case.execute(user_id)
        
        # Adaptar respuesta para el frontend
        return [{
            "conversation_id": c.conversation_id,
            "title": c.title,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "model": c.model,
            "agents": c.agents
        } for c in conversations]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
