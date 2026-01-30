"""
ATP v0.8.0 - Authentication System
================================
Sistema de autenticación JWT para WebSocket y API endpoints
"""

import jwt
import time
import uuid
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, WebSocket, WebSocketDisconnect, Query
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Generar secret seguro si no existe
if not JWT_SECRET_KEY or JWT_SECRET_KEY == "generar_una_clave_secreta_aqui":
    import secrets
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    print(f"⚠️ ADVERTENCIA: Generando JWT_SECRET_KEY temporal: {JWT_SECRET_KEY}")
    print("Por favor, establece JWT_SECRET_KEY en tus variables de entorno")

JWT_ALGORITHM = JWT_ALGORITHM or "HS256"
JWT_EXPIRATION_MINUTES = 60  # 1 hora
JWT_EXPIRATION_MINUTES_WS = 120  # 2 horas para WebSocket

class JWTManager:
    """Gestor de tokens JWT"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Crear token de acceso JWT"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4()),  # JWT ID para tracking
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_websocket_token(client_id: str, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token específico para WebSocket incluyendo ID de usuario"""
        to_encode = {
            "user_id": user_id,
            "client_id": client_id,
            "type": "websocket",
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4())
        }
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES_WS)
        
        to_encode["exp"] = expire
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    @staticmethod
    def verify_websocket_token(token: str) -> Dict[str, Any]:
        """Verificar token WebSocket"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # Verificar que sea un token WebSocket
            if payload.get("type") != "websocket":
                raise ValueError("Token no es de tipo WebSocket")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise WebSocketDisconnect(code=1008, reason="Token WebSocket expirado")
        except (InvalidTokenError, ValueError):
            raise WebSocketDisconnect(code=1008, reason="Token WebSocket inválido")

class SessionManager:
    """Gestor de sesiones activas"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.websocket_connections: Dict[str, WebSocket] = {}
    
    def create_session(self, client_id: str, user_info: Dict[str, Any]) -> str:
        """Crear nueva sesión"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "client_id": client_id,
            "user_info": user_info,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        self.active_sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtener información de sesión"""
        session = self.active_sessions.get(session_id)
        if session and session["is_active"]:
            # Actualizar última actividad
            session["last_activity"] = datetime.utcnow().isoformat()
            return session
        return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidar sesión"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["is_active"] = False
            # Remover conexión WebSocket si existe
            if session_id in self.websocket_connections:
                del self.websocket_connections[session_id]
            return True
        return False
    
    def register_websocket(self, session_id: str, websocket: WebSocket):
        """Registrar conexión WebSocket"""
        if session_id in self.active_sessions:
            self.websocket_connections[session_id] = websocket
            return True
        return False
    
    def unregister_websocket(self, session_id: str):
        """Desregistrar conexión WebSocket"""
        if session_id in self.websocket_connections:
            del self.websocket_connections[session_id]
    
    def cleanup_expired_sessions(self):
        """Limpiar sesiones expiradas"""
        now = datetime.utcnow()
        expired_sessions = []
        
        for session_id, session_data in self.active_sessions.items():
            last_activity = datetime.fromisoformat(session_data["last_activity"])
            if now - last_activity > timedelta(hours=2):  # 2 horas de inactividad
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.invalidate_session(session_id)
        
        return len(expired_sessions)
    
    def get_active_sessions_count(self) -> int:
        """Obtener conteo de sesiones activas"""
        return sum(1 for s in self.active_sessions.values() if s["is_active"])
    
    def get_websocket_connections_count(self) -> int:
        """Obtener conteo de conexiones WebSocket activas"""
        return len(self.websocket_connections)

# Instancias globales
jwt_manager = JWTManager()
session_manager = SessionManager()

# Decoradores de autenticación
def require_auth_token(token: str) -> Dict[str, Any]:
    """Requerir token de autenticación"""
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Remover "Bearer " si existe
    if token.startswith("Bearer "):
        token = token[7:]
    
    return jwt_manager.verify_token(token)

def require_websocket_auth(token: str = Query(...)) -> Dict[str, Any]:
    """Requerir token WebSocket"""
    if not token:
        raise WebSocketDisconnect(code=1008, reason="Token WebSocket requerido")
    
    return jwt_manager.verify_websocket_token(token)

# Middleware de autenticación para WebSocket
async def websocket_auth_middleware(websocket: WebSocket, token: str) -> Dict[str, Any]:
    """Middleware de autenticación para WebSocket"""
    try:
        # Verificar token
        payload = jwt_manager.verify_websocket_token(token)
        client_id = payload.get("client_id")
        user_id = payload.get("user_id")
        
        if not client_id:
            raise WebSocketDisconnect(code=1008, reason="Client ID requerido")
        
        # Crear o recuperar sesión vinculada al usuario
        user_info = {
            "user_id": user_id,
            "client_id": client_id,
            "connected_at": datetime.utcnow().isoformat(),
            "ip_address": websocket.client.host if websocket.client else "unknown"
        }
        
        session_id = session_manager.create_session(client_id, user_info)
        
        # Registrar conexión WebSocket
        session_manager.register_websocket(session_id, websocket)
        
        return {
            "session_id": session_id,
            "client_id": client_id,
            "user_id": user_id,
            "payload": payload
        }
        
    except Exception as e:
        print(f"Error en autenticación WebSocket: {e}")
        raise WebSocketDisconnect(code=1008, reason="Autenticación fallida")

# Funciones utilitarias
def generate_client_id() -> str:
    """Generar ID de cliente único"""
    return f"client_{int(time.time())}_{uuid.uuid4().hex[:8]}"

def is_token_expired(payload: Dict[str, Any]) -> bool:
    """Verificar si token está expirado"""
    exp = payload.get("exp")
    if not exp:
        return True
    
    return datetime.utcnow().timestamp() > exp

# Exportaciones
__all__ = [
    'JWTManager',
    'SessionManager', 
    'jwt_manager',
    'session_manager',
    'require_auth_token',
    'require_websocket_auth',
    'websocket_auth_middleware',
    'generate_client_id',
    'is_token_expired'
]
