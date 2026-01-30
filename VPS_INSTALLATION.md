# ATP v0.7.2 - Guía de Instalación en VPS

## 🚀 Requisitos Previos

- **VPS con Ubuntu 20.04+** (mínimo 2GB RAM, 1 CPU)
- **Dominio** (opcional, recomendado para SSL)
- **API Keys**:
  - Groq API Key (gratis): https://console.groq.com
  - OpenAI API Key (opcional): https://platform.openai.com

## 📋 Instalación Automática (Recomendada)

### 1. Conectar al VPS
```bash
ssh tu_usuario@tu_ip_vps
```

### 2. Ejecutar Script de Instalación
```bash
# Descargar y ejecutar script
wget https://raw.githubusercontent.com/LATINALU/ATP/main/scripts/install-vps.sh
chmod +x install-vps.sh
./install-vps.sh
```

El script instalará automáticamente:
- ✅ Docker y Docker Compose
- ✅ Nginx con configuración optimizada
- ✅ ATP v0.7.2 completo
- ✅ SSL con Let's Encrypt (si tienes dominio)
- ✅ Firewall y seguridad básica

## 🔧 Instalación Manual

### 1. Actualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependencias
```bash
sudo apt install -y curl wget git nginx certbot python3-certbot-nginx docker.io docker-compose
```

### 3. Configurar Docker
```bash
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### 4. Clonar Repositorio
```bash
git clone https://github.com/LATINALU/ATP.git
cd ATP
```

### 5. Configurar Variables de Entorno
```bash
cp .env.example .env
nano .env
```

**Configurar obligatorio:**
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Opcional
```

### 6. Configurar Dominio (opcional)
Si tienes dominio, actualiza `docker-compose.prod.yml`:
```yaml
environment:
  - NEXT_PUBLIC_API_URL=http://tu-dominio.com:8001
```

### 7. Configurar SSL (si tienes dominio)
```bash
sudo certbot --nginx -d tu-dominio.com --email admin@tu-dominio.com --redirect
```

### 8. Levantar Servicios
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## 🌐 Acceso a la Aplicación

### Con Dominio y SSL
- **Frontend**: https://tu-dominio.com
- **Backend API**: https://tu-dominio.com/api/

### Sin Dominio (IP directa)
- **Frontend**: http://tu-ip:3001
- **Backend API**: http://tu-ip:8001

## 📊 Verificación

### Verificar Estado
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Verificar Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Health Checks
```bash
# Backend
curl http://localhost:8001/health

# Frontend
curl http://localhost:3001
```

## 🔧 Gestión del Servicio

### Reiniciar Servicios
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Detener Servicios
```bash
docker-compose -f docker-compose.prod.yml down
```

### Actualizar ATP
```bash
cd ATP
git pull origin main
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## 🛡️ Seguridad

### Firewall
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Certificados SSL (Renovación automática)
```bash
# Certbot renueva automáticamente, pero puedes verificar:
sudo certbot renew --dry-run
```

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Contenedores no inician
```bash
# Ver logs específicos
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

#### 2. Error de API Key
```bash
# Verificar .env
cat .env
# Asegurar que las API keys son correctas
```

#### 3. Problemas de SSL
```bash
# Verificar estado de certbot
sudo certbot certificates
# Reemitir certificado
sudo certbot --nginx -d tu-dominio.com --force-renewal
```

#### 4. Alto uso de memoria
```bash
# Limitar recursos en docker-compose.prod.yml
deploy:
  resources:
    limits:
      memory: 1G
```

## 📈 Monitoreo

### Uso de Recursos
```bash
# Docker stats
docker stats

# Uso de disco
df -h

# Uso de memoria
free -h
```

### Logs del Sistema
```bash
# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker
sudo journalctl -u docker
```

## 🚀 Optimizaciones

### 1. Configurar Swap (si poca RAM)
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 2. Optimizar Nginx
Editar `/etc/nginx/nginx.conf` para ajustar:
- `worker_processes auto`
- `worker_connections 2048`

### 3. Configurar Backup
```bash
# Script de backup simple
#!/bin/bash
docker-compose -f docker-compose.prod.yml exec backend python -c "
import shutil
shutil.copytree('/app/data', '/backup/data')
"
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `docker-compose logs`
2. Verifica la configuración: `.env` y `docker-compose.prod.yml`
3. Consulta la documentación: https://github.com/LATINALU/ATP

---

**Versión**: ATP v0.7.2  
**Última actualización**: Enero 2026
