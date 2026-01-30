#!/bin/bash

# ATP Platform v0.8.1 - VPS Deployment Script
# Ubuntu 24.04 - http://atp-app.duckdns.org

set -e

echo "🚀 ATP Platform Deployment Starting..."

# 1. Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# 2. Install required packages
echo "🔧 Installing Docker and dependencies..."
apt install -y docker.io unzip curl wget git

# 3. Start Docker
echo "🐳 Starting Docker service..."
systemctl enable docker
systemctl start docker

# 4. Download ATP Platform
echo "⬇️ Downloading ATP Platform..."
cd /root
rm -rf ATPE
wget https://github.com/LATINALU/ATPE/archive/refs/heads/main.zip -O atp.zip
unzip atp.zip
mv ATPE-main ATPE
rm atp.zip

# 5. Setup environment
echo "⚙️ Setting up environment..."
cd ATPE
cp .env.production .env

# 6. Deploy with Docker Compose
echo "🚀 Deploying ATP Platform..."
docker compose -f docker-compose.prod.yml up -d --build

# 7. Health checks
echo "🔍 Running health checks..."
sleep 10

echo "📊 Container Status:"
docker compose -f docker-compose.prod.yml ps

echo ""
echo "🌐 Testing URLs..."
curl -I http://localhost:3000 || echo "❌ Frontend not responding"
curl http://localhost:8001/api/health || echo "❌ Backend not responding"

echo ""
echo "✅ ATP Platform Deployment Complete!"
echo "🌐 Frontend: http://atp-app.duckdns.org:3000"
echo "🔧 Backend API: http://atp-app.duckdns.org:8001"
echo "📊 Health Check: http://atp-app.duckdns.org:8001/api/health"
echo ""
echo "🔍 Logs: docker compose -f docker-compose.prod.yml logs -f"
