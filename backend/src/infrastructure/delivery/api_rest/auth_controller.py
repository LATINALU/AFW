from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
from src.domain.ports.input.auth_use_cases import LoginUseCasePort, LoginInputDTO, RegisterUseCasePort, RegisterInputDTO
from src.infrastructure.config.container import get_login_use_case, get_register_use_case, get_user_repository
from src.domain.exceptions.domain_exceptions import UnauthorizedException, ValidationException
from app.auth import jwt_manager, generate_client_id
from app.database import SubscriptionPlan, UserRole
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "free"

@router.post("/register")
async def register(
    request: RegisterRequest,
    use_case: RegisterUseCasePort = Depends(get_register_use_case)
):
    try:
        result = await use_case.execute(RegisterInputDTO(
            username=request.username,
            email=request.email,
            password=request.password
        ))
        return result
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(
    request: LoginRequest,
    use_case: LoginUseCasePort = Depends(get_login_use_case)
):
    try:
        result = await use_case.execute(LoginInputDTO(
            username=request.username,
            password=request.password
        ))
        return result
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_me(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        repo = get_user_repository()
        user = repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "user_code": user.user_code,
            "is_active": user.is_active
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/websocket-token")
async def create_websocket_token(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        client_id = generate_client_id()
        ws_token = jwt_manager.create_websocket_token(
            client_id=client_id,
            user_id=user_id,
            expires_delta=timedelta(hours=2)
        )
        
        return {
            "ws_token": ws_token,
            "client_id": client_id,
            "expires_in": 7200
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/usage")
async def get_usage(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("user_id")
        
        # Por ahora usamos el fallback a db directo ya que no tenemos un caso de uso de límites refinado
        from app.database import db
        user = db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        limits = db.check_query_limit(user_id)
        plan = SubscriptionPlan.ADMIN if user['role'] == UserRole.ADMIN else \
               SubscriptionPlan.PREMIUM if user['role'] == UserRole.PREMIUM else \
               SubscriptionPlan.FREE
               
        return {
            "allowed": limits["allowed"],
            "queries_used": limits["queries_used"],
            "queries_limit": limits["queries_limit"],
            "queries_remaining": limits["queries_remaining"],
            "plan_name": plan["name"],
            "plan_features": plan["features"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plans")
async def get_plans():
    return {
        "plans": [
            SubscriptionPlan.FREE,
            SubscriptionPlan.PREMIUM
        ]
    }

# Rutas de administración (legacy adapters for now)
@router.get("/admin/users")
async def admin_get_users(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt_manager.verify_token(token)
        admin_id = payload.get("user_id")
        
        from app.database import db
        user = db.get_user_by_id(admin_id)
        if not user or user['role'] != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Forbidden")
            
        users = db.get_all_users(admin_id)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
