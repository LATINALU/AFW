"""
Admin Authentication System
============================
Sistema robusto de autenticación para panel de administración
"""

import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

security = HTTPBasic()

class AdminAuth:
    def __init__(self):
        # Generar credenciales robustas si no existen
        self.admin_username = os.getenv("ADMIN_USERNAME", self._generate_secure_username())
        self.admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH", self._hash_password(self._generate_secure_password()))
        
        # Tokens de sesión activos
        self.active_sessions = {}
        self.session_duration = 3600  # 1 hora
        
        # Log de intentos de acceso
        self.access_attempts = {}
        
    def _generate_secure_username(self) -> str:
        """Generar username seguro"""
        return f"admin_{secrets.token_hex(8)}"
    
    def _generate_secure_password(self) -> str:
        """Generar contraseña robusta de 32 caracteres"""
        # Combinación de letras, números y símbolos
        password = secrets.token_urlsafe(32)
        print(f"\n{'='*60}")
        print(f"ADMIN CREDENTIALS GENERATED")
        print(f"{'='*60}")
        print(f"Username: {self.admin_username}")
        print(f"Password: {password}")
        print(f"{'='*60}")
        print(f"SAVE THESE CREDENTIALS SECURELY!")
        print(f"{'='*60}\n")
        return password
    
    def _hash_password(self, password: str) -> str:
        """Hash seguro de contraseña con salt"""
        salt = secrets.token_hex(32)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash"""
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hmac.compare_digest(new_hash.hex(), pwd_hash)
        except:
            return False
    
    def create_session_token(self, username: str) -> str:
        """Crear token de sesión"""
        token = secrets.token_urlsafe(32)
        self.active_sessions[token] = {
            'username': username,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.session_duration)
        }
        return token
    
    def verify_session_token(self, token: str) -> bool:
        """Verificar token de sesión"""
        if token not in self.active_sessions:
            return False
        
        session = self.active_sessions[token]
        if datetime.now() > session['expires_at']:
            del self.active_sessions[token]
            return False
        
        return True
    
    def authenticate(self, credentials: HTTPBasicCredentials) -> str:
        """Autenticar usuario y retornar token"""
        username = credentials.username
        password = credentials.password
        
        # Verificar credenciales
        if username != self.admin_username:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not self._verify_password(password, self.admin_password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Crear sesión
        return self.create_session_token(username)
    
    def require_admin(self, authorization: Optional[str] = Header(None)):
        """Middleware para requerir autenticación admin"""
        if not authorization:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != 'bearer':
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            
            if not self.verify_session_token(token):
                raise HTTPException(status_code=401, detail="Invalid or expired session")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

# Instancia global
admin_auth = AdminAuth()
