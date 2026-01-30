#!/bin/bash

# ATP v0.7.2 - Script de Instalación en VPS
# Uso: ./install-vps.sh

set -e

echo "🚀 ATP v0.7.2 - Instalación en VPS"
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones de utilidad
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   log_error "No ejecutar como root. Ejecutar como usuario normal."
   exit 1
fi

# Actualizar sistema
log_info "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
log_info "Instalando dependencias..."
sudo apt install -y curl wget git nginx certbot python3-certbot-nginx docker.io docker-compose

# Habilitar Docker
log_info "Configurando Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Clonar repositorio
log_info "Clonando ATP desde GitHub..."
if [ -d "ATP" ]; then
    log_warn "Directorio ATP existe, eliminando..."
    rm -rf ATP
fi

git clone https://github.com/LATINALU/ATP.git
cd ATP

# Crear archivo .env
log_info "Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_warn "⚠️  IMPORTANTE: Editar .env con tus API keys!"
    log_warn "   - GROQ_API_KEY: Obtener de https://console.groq.com"
    log_warn "   - OPENAI_API_KEY: Opcional, de https://platform.openai.com"
    echo ""
    read -p "¿Deseas editar .env ahora? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        nano .env
    fi
fi

# Configurar dominio (opcional)
log_info "Configuración de dominio..."
read -p "¿Tienes un dominio? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Ingresa tu dominio (ej: atp-app.duckdns.org): " DOMAIN
    if [ ! -z "$DOMAIN" ]; then
        # Actualizar docker-compose.prod.yml con el dominio
        sed -i "s|atp-app.duckdns.org|$DOMAIN|g" docker-compose.prod.yml
        log_info "Dominio configurado: $DOMAIN"
        
        # Configurar SSL con Let's Encrypt
        log_info "Configurando SSL con Let's Encrypt..."
        sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN --redirect
    fi
else
    log_warn "Sin dominio configurado. Usando IP directa."
    # Actualizar docker-compose para usar IP
    SERVER_IP=$(curl -s ifconfig.me)
    sed -i "s|atp-app.duckdns.org|$SERVER_IP|g" docker-compose.prod.yml
    log_info "IP configurada: $SERVER_IP"
fi

# Construir y levantar contenedores
log_info "Construyendo y levantando contenedores Docker..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que los servicios estén listos
log_info "Esperando a que los servicios inicien..."
sleep 30

# Verificar estado
log_info "Verificando estado de los servicios..."
docker-compose -f docker-compose.prod.yml ps

# Mostrar información de acceso
echo ""
echo "🎉 ¡Instalación completada!"
echo "=========================="
if [ ! -z "$DOMAIN" ]; then
    echo "🌐 Frontend: https://$DOMAIN"
    echo "🔧 Backend API: https://$DOMAIN:8001"
else
    SERVER_IP=$(curl -s ifconfig.me)
    echo "🌐 Frontend: http://$SERVER_IP:3001"
    echo "🔧 Backend API: http://$SERVER_IP:8001"
fi

echo ""
echo "📋 Comandos útiles:"
echo "  Ver logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  Detener: docker-compose -f docker-compose.prod.yml down"
echo "  Reiniciar: docker-compose -f docker-compose.prod.yml restart"
echo ""

# Verificar health checks
log_info "Verificando health checks..."
sleep 10

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    log_info "✅ Backend saludable"
else
    log_warn "⚠️  Backend no responde (puede estar iniciando)"
fi

if curl -f http://localhost:3001 > /dev/null 2>&1; then
    log_info "✅ Frontend saludable"
else
    log_warn "⚠️  Frontend no responde (puede estar iniciando)"
fi

echo ""
log_info "🔥 ATP v0.7.2 está instalado y funcionando!"
log_warn "📝 No olvides configurar tus API keys en .env si no lo hiciste"
