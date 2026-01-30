"""
ATP v0.8.0 - Security Validators
=================================
Validación y sanitización de inputs para prevenir ataques
"""

import re
import html
import json
from typing import Any, Dict, List, Optional
from pydantic import validator, Field
import bleach
from urllib.parse import urlparse

# Configuración de bleach para HTML sanitización
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'code', 'pre', 
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href', 'title'],
    'code': ['class']
}

class SecurityValidator:
    """Clase principal para validación de seguridad"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Sanitizar HTML para prevenir XSS"""
        if not text:
            return ""
        
        # Usar bleach para limpiar HTML
        clean_html = bleach.clean(
            text, 
            tags=ALLOWED_TAGS, 
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        return clean_html
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitizar texto plano"""
        if not text:
            return ""
        
        # Escapar HTML entities
        sanitized = html.escape(text)
        
        # Remover caracteres de control peligrosos
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', sanitized)
        
        # Limitar longitud
        max_length = 10000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."
        
        return sanitized.strip()
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validar URL segura"""
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                parsed.netloc and
                not any(char in parsed.netloc for char in ['<', '>', '"', "'", '&'])
            )
        except:
            return False
    
    @staticmethod
    def validate_json(data: str) -> Optional[Dict]:
        """Validar y parsear JSON de forma segura"""
        if not data:
            return None
        
        try:
            # Limitar tamaño del JSON
            if len(data) > 1000000:  # 1MB
                return None
            
            parsed = json.loads(data)
            
            # Verificar que no haya objetos anidados muy profundos
            max_depth = 10
            def check_depth(obj, current_depth=0):
                if current_depth > max_depth:
                    raise ValueError("JSON too deep")
                if isinstance(obj, dict):
                    for value in obj.values():
                        check_depth(value, current_depth + 1)
                elif isinstance(obj, list):
                    for item in obj:
                        check_depth(item, current_depth + 1)
            
            check_depth(parsed)
            return parsed
        except:
            return None
    
    @staticmethod
    def validate_agent_list(agents: List[str]) -> List[str]:
        """Validar lista de agentes - Usa AGENT_REGISTRY con 120 agentes"""
        if not agents:
            return []
        
        # Obtener lista de agentes permitidos desde el registry
        try:
            from app.agents.agent_registry import get_registered_agents
            allowed_agents = set(get_registered_agents().keys())
        except ImportError:
            # Fallback si no se puede importar
            from app.agents.registry import AGENT_DEFINITIONS
            allowed_agents = set(AGENT_DEFINITIONS.keys())
        
        # Validar y limpiar lista
        valid_agents = []
        for agent in agents:
            if isinstance(agent, str):
                agent_clean = agent.strip()
                # Verificar exactamente como viene (sin lowercase)
                if agent_clean in allowed_agents and agent_clean not in valid_agents:
                    valid_agents.append(agent_clean)
        
        # Limitar a máximo 10 agentes (aumentado de 5 para tareas complejas)
        return valid_agents[:10]
    
    @staticmethod
    def validate_model_name(model: str) -> str:
        """Validar nombre de modelo"""
        if not model:
            return "groq-default"  # Default seguro
        
        # Patrones permitidos
        allowed_patterns = [
            r'^[a-zA-Z0-9_\-/\.]+$',  # Alfanumérico con algunos caracteres especiales
        ]
        
        for pattern in allowed_patterns:
            if re.match(pattern, model):
                return model.strip()
        
        return "groq-default"  # Default si no es válido
    
    @staticmethod
    def detect_suspicious_content(text: str) -> List[str]:
        """Detectar contenido sospechoso"""
        suspicious_patterns = [
            r'<script[^>]*>.*?</script>',  # Scripts
            r'javascript:',  # Protocolos peligrosos
            r'vbscript:',   # VBScript
            r'on\w+\s*=',   # Event handlers
            r'eval\s*\(',   # eval()
            r'document\.',  # Acceso a documento
            r'window\.',    # Acceso a window
        ]
        
        threats = []
        text_lower = text.lower()
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
                threats.append(f"Patrón sospechoso detectado: {pattern}")
        
        return threats
    
    @staticmethod
    def validate_api_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Validar configuración de API"""
        if not isinstance(config, dict):
            return {}
        
        valid_config = {}
        
        # Validar tipo
        if config.get('type') in ['groq', 'openai', 'anthropic', 'local']:
            valid_config['type'] = config['type']
        
        # Validar API key (sin validar contenido, solo formato)
        api_key = config.get('apiKey', '')
        if isinstance(api_key, str) and 20 <= len(api_key) <= 200:
            valid_config['apiKey'] = api_key
        
        # Validar base URL
        base_url = config.get('baseUrl', '')
        if isinstance(base_url, str) and SecurityValidator.validate_url(base_url):
            valid_config['baseUrl'] = base_url
        
        return valid_config

# Funciones de validación para Pydantic
def validate_message_input(message: str) -> str:
    """Validador para mensajes de usuario"""
    if not message:
        raise ValueError("El mensaje no puede estar vacío")
    
    if len(message) > 10000:
        raise ValueError("El mensaje es demasiado largo (máximo 10,000 caracteres)")
    
    # Detectar contenido sospechoso
    threats = SecurityValidator.detect_suspicious_content(message)
    if threats:
        raise ValueError(f"Contenido no permitido detectado")
    
    # Sanitizar
    return SecurityValidator.sanitize_text(message)

def validate_agents_input(agents: List[str]) -> List[str]:
    """Validador para lista de agentes"""
    if not agents:
        raise ValueError("Debe seleccionar al menos un agente")
    
    valid_agents = SecurityValidator.validate_agent_list(agents)
    
    if len(valid_agents) == 0:
        raise ValueError("No se seleccionaron agentes válidos")
    
    if len(valid_agents) > 5:
        raise ValueError("Máximo 5 agentes permitidos")
    
    return valid_agents

def validate_model_input(model: str) -> str:
    """Validador para nombre de modelo"""
    if not model:
        return "groq-default"
    
    return SecurityValidator.validate_model_name(model)

def validate_api_config_input(config: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Validador para configuración de API"""
    if not config:
        return None
    
    return SecurityValidator.validate_api_config(config)

# Middleware de sanitización
class SecurityMiddleware:
    """Middleware para aplicar validaciones de seguridad"""
    
    @staticmethod
    def sanitize_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizar datos de request"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                if key == 'message':
                    sanitized[key] = SecurityValidator.sanitize_text(value)
                elif key == 'model':
                    sanitized[key] = SecurityValidator.validate_model_name(value)
                else:
                    sanitized[key] = SecurityValidator.sanitize_text(value)
            elif isinstance(value, list):
                if key == 'agents':
                    sanitized[key] = SecurityValidator.validate_agent_list(value)
                else:
                    sanitized[key] = value  # Mantener otras listas
            elif isinstance(value, dict):
                if key == 'apiConfig':
                    sanitized[key] = SecurityValidator.validate_api_config(value)
                else:
                    sanitized[key] = value  # Mantener otros dicts
            else:
                sanitized[key] = value
        
        return sanitized

# Exportaciones
__all__ = [
    'SecurityValidator',
    'validate_message_input',
    'validate_agents_input', 
    'validate_model_input',
    'validate_api_config_input',
    'SecurityMiddleware'
]
