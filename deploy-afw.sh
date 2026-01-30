#!/bin/bash

# AFW Deployment Script
# This script deploys the AFW project with unique ports and configuration

set -e

echo "🚀 Starting AFW Deployment..."

# Load environment variables
if [ -f .env.afw ]; then
    export $(cat .env.afw | grep -v '^#' | xargs)
    echo "✅ Loaded .env.afw configuration"
else
    echo "⚠️  Warning: .env.afw not found, using defaults"
fi

# Stop any existing AFW containers
echo "🛑 Stopping existing AFW containers..."
docker-compose -f docker-compose.afw.yml down 2>/dev/null || true

# Remove old AFW containers if they exist
echo "🧹 Cleaning up old containers..."
docker rm -f afw-backend afw-frontend afw-redis 2>/dev/null || true

# Prune unused networks
echo "🌐 Cleaning up networks..."
docker network prune -f

# Build and start AFW services
echo "🔨 Building and starting AFW services..."
docker-compose -f docker-compose.afw.yml up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose -f docker-compose.afw.yml ps

# Test backend health
echo "🏥 Testing backend health..."
curl -f http://localhost:${AFW_BACKEND_PORT:-8002}/api/health || echo "⚠️  Backend health check failed"

# Test frontend (wait longer for production build)
echo "🎨 Testing frontend..."
sleep 20
curl -f http://localhost:${AFW_FRONTEND_PORT:-3002} || echo "⚠️  Frontend check failed"

echo ""
echo "✅ AFW Deployment Complete!"
echo ""
echo "📍 Services running on:"
echo "   - Frontend: http://localhost:${AFW_FRONTEND_PORT:-3002}"
echo "   - Backend:  http://localhost:${AFW_BACKEND_PORT:-8002}"
echo "   - Redis:    localhost:${AFW_REDIS_PORT:-6380}"
echo ""
echo "🌐 Public URL: http://${AFW_DOMAIN:-afw-app.duckdns.org}"
echo ""
