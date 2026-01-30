# ATP v0.8.0 - Docker Deployment Guide
=====================================

## 🐳 Docker Compose Files

### Available Configurations

1. **Development**: `docker-compose.dev.yml`
2. **Production**: `docker-compose.production.yml`
3. **Default**: `docker-compose.yml` (with optional Nginx)

## 🚀 Quick Start

### Development Environment
```bash
# Generate secrets first
cd scripts
python generate_secrets.py

# Copy environment files
cp ../.env.example ../.env.dev

# Start development stack
cd ..
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Production Environment
```bash
# Generate production secrets
cd scripts
python generate_secrets.py

# Copy production environment
cp ../.env.production ../.env

# Start production stack
cd ..
docker-compose -f docker-compose.production.yml up -d

# View logs
docker-compose -f docker-compose.production.yml logs -f
```

## 🔧 Environment Variables

### Required for Production
```bash
JWT_SECRET_KEY=your_jwt_secret_here
SESSION_SECRET=your_session_secret_here
ENCRYPTION_KEY=your_encryption_key_here
API_SECRET_KEY=your_api_secret_here
REDIS_KEY=your_redis_key_here
```

### Optional
```bash
FRONTEND_URL=https://your-domain.com
RATE_LIMIT_ENABLED=true
CORS_MAX_AGE=86400
```

## 📊 Services Overview

### Backend (atp-backend-v0.8.0)
- **Port**: 8001
- **Features**: Security, Rate Limiting, JWT Auth
- **Health Check**: `/api/health`
- **Dependencies**: Redis

### Frontend (atp-frontend-v0.8.0)
- **Port**: 3000
- **Features**: Responsive Design, SecureStorage
- **Health Check**: `/`
- **Dependencies**: Backend

### Redis (atp-redis-v0.8.0)
- **Port**: 6379
- **Features**: Rate Limiting, Session Storage
- **Memory Limit**: 256MB
- **Persistence**: RDB snapshots

### Nginx (Optional)
- **Ports**: 80, 443
- **Features**: Reverse Proxy, SSL Termination
- **Profile**: Production only

## 🔍 Health Checks

All services include health checks:

```bash
# Check all services
docker-compose ps

# Check specific service health
docker-compose exec backend curl -f http://localhost:8001/api/health
docker-compose exec redis redis-cli ping
docker-compose exec frontend curl -f http://localhost:3000
```

## 📈 Monitoring

### Resource Limits
- **Backend**: 2 CPU, 2GB RAM (Production)
- **Frontend**: 1 CPU, 1GB RAM (Production)
- **Redis**: 1 CPU, 512MB RAM (Production)
- **Nginx**: 0.5 CPU, 256MB RAM (Production)

### Logs
```bash
# View all logs
docker-compose logs

# Follow specific service
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend
```

## 🔄 Scaling

### Horizontal Scaling
```bash
# Scale backend
docker-compose -f docker-compose.production.yml up -d --scale backend=3

# Scale frontend
docker-compose -f docker-compose.production.yml up -d --scale frontend=2
```

### Vertical Scaling
Edit `docker-compose.production.yml` and adjust `deploy.resources` limits.

## 🔒 Security Features

### v0.8.0 Security
- ✅ JWT Authentication
- ✅ Rate Limiting with Redis
- ✅ Input Validation & Sanitization
- ✅ CORS Configuration
- ✅ Encrypted Storage
- ✅ Session Management

### Network Security
- ✅ Isolated Docker Network
- ✅ Internal Service Communication
- ✅ No Exposed Internal Ports
- ✅ SSL Termination at Nginx

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :8001
   
   # Change ports in docker-compose.yml
   ```

2. **Permission Issues**
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER ./backend ./frontend
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase limits in docker-compose.yml
   ```

4. **Redis Connection**
   ```bash
   # Test Redis connection
   docker-compose exec redis redis-cli ping
   
   # Check Redis logs
   docker-compose logs redis
   ```

### Debug Mode

Enable debug logging:
```bash
# Set DEBUG=true in environment
DEBUG=true docker-compose -f docker-compose.dev.yml up -d

# View detailed logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

## 📝 Maintenance

### Updates
```bash
# Pull latest images
docker-compose pull

# Recreate services
docker-compose up -d --force-recreate
```

### Backups
```bash
# Backup Redis data
docker-compose exec redis redis-cli BGSAVE
docker cp atp-redis-prod-v0.8.0:/data/dump.rdb ./backup/

# Backup environment files
cp .env.production ./backup/
```

### Cleanup
```bash
# Remove stopped containers
docker-compose rm -f

# Remove unused images
docker image prune -f

# Remove unused volumes (careful!)
docker volume prune -f
```

## 🌐 Production Deployment

### SSL Certificate Setup
1. Place SSL certificates in `./ssl/`
2. Update `nginx.prod.conf` with your domain
3. Set FRONTEND_URL environment variable

### Domain Configuration
```bash
# Update environment
FRONTEND_URL=https://your-domain.com

# Update nginx configuration
# Edit nginx.prod.conf
```

### Monitoring Setup
Consider adding:
- Prometheus for metrics
- Grafana for dashboards
- ELK stack for logging

## 📞 Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify health: `docker-compose ps`
3. Test connectivity: `docker-compose exec`
4. Review configuration: Environment variables
