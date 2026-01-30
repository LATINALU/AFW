#!/usr/bin/env python3
"""
ATP v0.8.0 - Secure Secrets Generator
====================================
Generador de secrets seguros para producción
"""

import secrets
import string
import hashlib
import os
from datetime import datetime

class SecureSecretGenerator:
    """Generador de secrets criptográficamente seguros"""
    
    @staticmethod
    def generate_jwt_secret(length: int = 64) -> str:
        """Generar secret para JWT"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_session_secret(length: int = 64) -> str:
        """Generar secret para sesiones"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """Generar API key segura"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_database_url(length: int = 32) -> str:
        """Generar string aleatorio para database URL"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_encryption_key(length: int = 32) -> str:
        """Generar clave de encriptación"""
        return secrets.token_hex(length)
    
    @staticmethod
    def generate_password(length: int = 32, use_symbols: bool = True) -> str:
        """Generar contraseña segura"""
        chars = string.ascii_letters + string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_redis_key(length: int = 32) -> str:
        """Generar clave para Redis"""
        return secrets.token_hex(length)

def generate_env_file():
    """Genera archivo .env con secrets seguros"""
    
    print("🔐 ATP v0.8.0 - Generador de Secrets Seguros")
    print("=" * 50)
    
    # Generar todos los secrets
    secrets_data = {
        "JWT_SECRET_KEY": SecureSecretGenerator.generate_jwt_secret(),
        "SESSION_SECRET": SecureSecretGenerator.generate_session_secret(),
        "ENCRYPTION_KEY": SecureSecretGenerator.generate_encryption_key(),
        "REDIS_KEY": SecureSecretGenerator.generate_redis_key(),
        "DATABASE_PASSWORD": SecureSecretGenerator.generate_password(24),
        "API_SECRET_KEY": SecureSecretGenerator.generate_api_key(),
    }
    
    # Generar .env.example con placeholders
    env_example = f"""# ATP v0.8.0 - Environment Variables (Seguro)
# ================================================
# Generado automáticamente: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ⚠️  COPIA ESTOS VALORES EN TU ARCHIVO .env REAL ⚠️

# 🔐 Secrets Críticos (NO COMPARTIR)
JWT_SECRET_KEY={secrets_data["JWT_SECRET_KEY"]}
SESSION_SECRET={secrets_data["SESSION_SECRET"]}
ENCRYPTION_KEY={secrets_data["ENCRYPTION_KEY"]}

# 🔑 API Keys (Configurar con tus propias keys)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 🗄️ Base de Datos
DATABASE_URL=postgresql://user:{secrets_data["DATABASE_PASSWORD"]}@localhost:5432/atp
REDIS_URL=redis://localhost:6379
REDIS_KEY={secrets_data["REDIS_KEY"]}

# 🌐 Servidor
HOST=0.0.0.0
PORT=8001
DEBUG=false
ENVIRONMENT=development

# 🚀 Frontend
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_DEMO_MODE=false

# 🛡️ Seguridad
API_SECRET_KEY={secrets_data["API_SECRET_KEY"]}
CORS_MAX_AGE=86400
RATE_LIMIT_ENABLED=true

# 📊 Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/atp.log

# 🚀 Feature Flags
ENABLE_STREAMING=true
ENABLE_MEMORY=true
ENABLE_MULTI_PROVIDER=true
ENABLE_AUTH=true
ENABLE_RATE_LIMITING=true

# 🔔 WebSocket
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000
WS_TIMEOUT=300
"""

    # Generar .env.production con valores seguros
    env_production = f"""# ATP v0.8.0 - Production Environment Variables
# ==================================================
# ⚠️  ARCHIVO DE PRODUCCIÓN - MANTENER SECRETO ⚠️

# 🔐 Secrets Críticos (PRODUCCIÓN)
JWT_SECRET_KEY={secrets_data["JWT_SECRET_KEY"]}
SESSION_SECRET={secrets_data["SESSION_SECRET"]}
ENCRYPTION_KEY={secrets_data["ENCRYPTION_KEY"]}

# 🔑 API Keys (Configurar con keys reales de producción)
GROQ_API_KEY=YOUR_PROD_GROQ_KEY_HERE
OPENAI_API_KEY=YOUR_PROD_OPENAI_KEY_HERE
ANTHROPIC_API_KEY=YOUR_PROD_ANTHROPIC_KEY_HERE

# 🗄️ Base de Datos (Producción)
DATABASE_URL=postgresql://user:{secrets_data["DATABASE_PASSWORD"]}@your-db-host:5432/atp_prod
REDIS_URL=redis://your-redis-host:6379
REDIS_KEY={secrets_data["REDIS_KEY"]}

# 🌐 Servidor (Producción)
HOST=0.0.0.0
PORT=8001
DEBUG=false
ENVIRONMENT=production

# 🚀 Frontend (Producción)
NEXT_PUBLIC_API_URL=https://api.atp.production.com
NEXT_PUBLIC_DEMO_MODE=false
FRONTEND_URL=https://atp.production.com

# 🛡️ Seguridad (Producción)
API_SECRET_KEY={secrets_data["API_SECRET_KEY"]}
CORS_MAX_AGE=86400
RATE_LIMIT_ENABLED=true

# 📊 Logging (Producción)
LOG_LEVEL=WARNING
LOG_FILE=/var/log/atp/atp.log

# 🚀 Feature Flags (Producción)
ENABLE_STREAMING=true
ENABLE_MEMORY=true
ENABLE_MULTI_PROVIDER=true
ENABLE_AUTH=true
ENABLE_RATE_LIMITING=true

# 🔔 WebSocket (Producción)
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000
WS_TIMEOUT=300
"""

    # Guardar archivos
    try:
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_example)
        print("✅ .env.example generado exitosamente")
        
        with open('.env.production', 'w', encoding='utf-8') as f:
            f.write(env_production)
        print("✅ .env.production generado exitosamente")
        
    except Exception as e:
        print(f"❌ Error guardando archivos: {e}")
        return
    
    # Mostrar resumen
    print("\n📋 Resumen de Secrets Generados:")
    print("-" * 40)
    for key, value in secrets_data.items():
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else value
        print(f"🔑 {key}: {masked}")
    
    print(f"\n📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔐 Entropía: {len(secrets_data['JWT_SECRET_KEY']) * 8} bits")
    
    print("\n⚠️  ACCIONES REQUERIDAS:")
    print("1. Copia .env.example a .env")
    print("2. Configura tus API keys reales en .env")
    print("3. Guarda .env.production en un lugar seguro")
    print("4. Nunca commits .env con secrets reales")
    
    print("\n🛡️ RECOMENDACIONES DE SEGURIDAD:")
    print("• Usa un gestor de secrets (AWS Secrets Manager, Vault)")
    print("• Rota los secrets cada 90 días")
    print("• Monitorea el acceso a los secrets")
    print("• Usa diferentes secrets para cada entorno")

def generate_docker_secrets():
    """Genera secrets para Docker Swarm/Kubernetes"""
    
    print("\n🐳 Generando Secrets para Docker...")
    
    docker_secrets = {
        "jwt_secret": SecureSecretGenerator.generate_jwt_secret(),
        "session_secret": SecureSecretGenerator.generate_session_secret(),
        "encryption_key": SecureSecretGenerator.generate_encryption_key(),
        "redis_key": SecureSecretGenerator.generate_redis_key(),
        "db_password": SecureSecretGenerator.generate_password(24),
    }
    
    # Docker Compose secrets
    docker_compose_secrets = f"""# ATP v0.8.0 - Docker Secrets
# ================================
# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

version: '3.8'

secrets:
  jwt_secret:
    external: true
  session_secret:
    external: true
  encryption_key:
    external: true
  redis_key:
    external: true
  db_password:
    external: true

services:
  backend:
    build: ./backend
    secrets:
      - jwt_secret
      - session_secret
      - encryption_key
    environment:
      - JWT_SECRET_KEY_FILE=/run/secrets/jwt_secret
      - SESSION_SECRET_FILE=/run/secrets/session_secret
      - ENCRYPTION_KEY_FILE=/run/secrets/encryption_key
"""
    
    try:
        with open('docker-compose.secrets.yml', 'w', encoding='utf-8') as f:
            f.write(docker_compose_secrets)
        print("✅ docker-compose.secrets.yml generado")
        
        # Generar script para crear secrets
        with open('create-docker-secrets.sh', 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write("# ATP v0.8.0 - Crear Docker Secrets\n")
            f.write("# Generado: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
            
            for secret_name, secret_value in docker_secrets.items():
                f.write(f"echo '{secret_value}' | docker secret create {secret_name} -\n")
            
            f.write("\necho '✅ Todos los secrets de Docker creados'\n")
        
        os.chmod('create-docker-secrets.sh', 0o755)
        print("✅ create-docker-secrets.sh generado")
        
    except Exception as e:
        print(f"❌ Error generando Docker secrets: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando generación de secrets seguros para ATP v0.8.0")
    print()
    
    # Generar secrets para entorno
    generate_env_file()
    
    # Generar secrets para Docker
    generate_docker_secrets()
    
    print("\n🎉 Generación de secrets completada!")
    print("📁 Archivos generados:")
    print("   • .env.example (template para desarrollo)")
    print("   • .env.production (secrets de producción)")
    print("   • docker-compose.secrets.yml (Docker secrets)")
    print("   • create-docker-secrets.sh (script Docker)")

if __name__ == "__main__":
    main()
