"""
Rate Limiting & DDoS Protection
================================
Sistema de protección contra ataques de denegación de servicio
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import hashlib
import time

class RateLimiter:
    def __init__(self):
        # IP -> (request_count, window_start_time)
        self.ip_requests: Dict[str, Tuple[int, float]] = {}
        # IP -> (failed_attempts, last_attempt_time)
        self.failed_attempts: Dict[str, Tuple[int, float]] = {}
        # IP -> block_until_time
        self.blocked_ips: Dict[str, float] = {}
        
        # Configuración
        self.max_requests_per_minute = 60
        self.max_requests_per_hour = 1000
        self.max_failed_attempts = 10
        self.block_duration = 3600  # 1 hora
        self.window_size = 60  # 1 minuto
        
    def get_client_ip(self, request: Request) -> str:
        """Obtener IP real del cliente (considerando proxies)"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def is_blocked(self, ip: str) -> bool:
        """Verificar si una IP está bloqueada"""
        if ip in self.blocked_ips:
            if time.time() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False
    
    def check_rate_limit(self, ip: str) -> bool:
        """Verificar límite de tasa"""
        current_time = time.time()
        
        # Limpiar ventanas antiguas
        if ip in self.ip_requests:
            count, window_start = self.ip_requests[ip]
            if current_time - window_start > self.window_size:
                self.ip_requests[ip] = (1, current_time)
            else:
                self.ip_requests[ip] = (count + 1, window_start)
                if count + 1 > self.max_requests_per_minute:
                    return False
        else:
            self.ip_requests[ip] = (1, current_time)
        
        return True
    
    def record_failed_attempt(self, ip: str):
        """Registrar intento fallido"""
        current_time = time.time()
        
        if ip in self.failed_attempts:
            count, last_time = self.failed_attempts[ip]
            # Reset si pasó más de 1 hora
            if current_time - last_time > 3600:
                self.failed_attempts[ip] = (1, current_time)
            else:
                new_count = count + 1
                self.failed_attempts[ip] = (new_count, current_time)
                
                # Bloquear si excede intentos
                if new_count >= self.max_failed_attempts:
                    self.blocked_ips[ip] = current_time + self.block_duration
        else:
            self.failed_attempts[ip] = (1, current_time)
    
    async def __call__(self, request: Request):
        """Middleware de rate limiting"""
        ip = self.get_client_ip(request)
        
        # Verificar si está bloqueada
        if self.is_blocked(ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. IP temporarily blocked."
            )
        
        # Verificar rate limit
        if not self.check_rate_limit(ip):
            self.record_failed_attempt(ip)
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please slow down."
            )

# Instancia global
rate_limiter = RateLimiter()
