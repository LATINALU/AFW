# 🚀 ATP Platform v0.8.1 - Deployment Instructions

## 🌐 Public Domain Ready
**URL**: http://atp-app.duckdns.org:3000

## 📋 Two Deployment Options

### Option 1: Quick Script (Recommended)
```bash
# SSH to your VPS
ssh root@147.93.191.92

# Download and run deployment script
wget https://raw.githubusercontent.com/LATINALU/ATPE/main/deploy_vps.sh
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### Option 2: Manual Steps
```bash
# 1. Update system
apt update && apt upgrade -y

# 2. Install Docker
apt install -y docker.io unzip curl wget git
systemctl enable docker
systemctl start docker

# 3. Download ATP Platform
cd /root
wget https://github.com/LATINALU/ATPE/archive/refs/heads/main.zip -O atp.zip
unzip atp.zip
mv ATPE-main ATPE
rm atp.zip

# 4. Deploy
cd ATPE
cp .env.production .env
docker compose -f docker-compose.prod.yml up -d --build
```

## 🔧 Environment Configuration
- **Domain**: http://atp-app.duckdns.org
- **Frontend Port**: 3000
- **Backend Port**: 8001
- **WebSocket**: ws://atp-app.duckdns.org:8001/ws

## 📊 Health Checks
```bash
# Frontend
curl -I http://atp-app.duckdns.org:3000

# Backend Health
curl http://atp-app.duckdns.org:8001/api/health

# Docker Status
docker compose -f docker-compose.prod.yml ps
```

## 🎯 Features Ready
- ✅ 30 AI Agents
- ✅ Multi-user storage
- ✅ 10 themes with improved contrast
- ✅ Professional agent formatting
- ✅ WebSocket real-time chat
- ✅ Responsive design

## 🌐 Access URLs
- **Main App**: http://atp-app.duckdns.org:3000
- **API Health**: http://atp-app.duckdns.org:8001/api/health
- **WebSocket**: ws://atp-app.duckdns.org:8001/ws

## 🚀 Launch Ready!

Deploy now and your ATP Platform will be available worldwide! 🎉
