"""
Anti-Scraping Protection
=========================
Protección contra bots y scraping automatizado
"""

from fastapi import Request, HTTPException
from typing import Dict, Set
import time
import hashlib
import re

class AntiScrapingProtection:
    def __init__(self):
        # User-Agent patterns sospechosos
        self.suspicious_agents = [
            r'bot', r'crawler', r'spider', r'scraper', r'curl', r'wget',
            r'python-requests', r'scrapy', r'selenium', r'phantomjs'
        ]
        
        # IPs sospechosas (comportamiento de bot)
        self.suspicious_ips: Set[str] = set()
        
        # Fingerprints de requests
        self.request_fingerprints: Dict[str, list] = {}
        
        # Headers requeridos
        self.required_headers = ['user-agent', 'accept', 'accept-language']
        
    def get_request_fingerprint(self, request: Request) -> str:
        """Generar fingerprint único de la request"""
        components = [
            request.client.host if request.client else "unknown",
            request.headers.get("user-agent", ""),
            request.headers.get("accept", ""),
            request.headers.get("accept-language", ""),
            str(sorted(request.headers.keys()))
        ]
        fingerprint = hashlib.sha256("|".join(components).encode()).hexdigest()
        return fingerprint
    
    def is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Detectar User-Agent sospechoso"""
        if not user_agent:
            return True
        
        user_agent_lower = user_agent.lower()
        for pattern in self.suspicious_agents:
            if re.search(pattern, user_agent_lower):
                return True
        return False
    
    def check_required_headers(self, request: Request) -> bool:
        """Verificar headers requeridos"""
        for header in self.required_headers:
            if header not in request.headers:
                return False
        return True
    
    def detect_automated_behavior(self, ip: str, fingerprint: str) -> bool:
        """Detectar comportamiento automatizado"""
        current_time = time.time()
        
        if ip not in self.request_fingerprints:
            self.request_fingerprints[ip] = []
        
        # Agregar timestamp
        self.request_fingerprints[ip].append(current_time)
        
        # Limpiar requests antiguas (más de 1 minuto)
        self.request_fingerprints[ip] = [
            t for t in self.request_fingerprints[ip] 
            if current_time - t < 60
        ]
        
        # Detectar patrones sospechosos
        recent_requests = self.request_fingerprints[ip]
        
        # Demasiadas requests en poco tiempo (>30 en 1 minuto)
        if len(recent_requests) > 30:
            return True
        
        # Requests con intervalos muy regulares (bot)
        if len(recent_requests) >= 5:
            intervals = [
                recent_requests[i] - recent_requests[i-1] 
                for i in range(1, len(recent_requests))
            ]
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
            
            # Varianza muy baja = comportamiento de bot
            if variance < 0.1 and avg_interval < 2:
                return True
        
        return False
    
    async def __call__(self, request: Request):
        """Middleware de anti-scraping"""
        # Excluir rutas públicas específicas
        if request.url.path in ["/api/health", "/docs", "/openapi.json"]:
            return
        
        ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        
        # Verificar headers requeridos
        if not self.check_required_headers(request):
            raise HTTPException(
                status_code=403,
                detail="Missing required headers"
            )
        
        # Verificar User-Agent sospechoso
        if self.is_suspicious_user_agent(user_agent):
            raise HTTPException(
                status_code=403,
                detail="Suspicious user agent detected"
            )
        
        # Generar fingerprint y detectar comportamiento automatizado
        fingerprint = self.get_request_fingerprint(request)
        if self.detect_automated_behavior(ip, fingerprint):
            self.suspicious_ips.add(ip)
            raise HTTPException(
                status_code=429,
                detail="Automated behavior detected"
            )

# Instancia global
anti_scraping = AntiScrapingProtection()
