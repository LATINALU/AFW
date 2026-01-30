# Docker Structure v1.0.0

## Overview
Restructured Docker configuration for ATP project with consolidated and optimized setup.

## File Structure

### Main Configuration Files
- `docker-compose.yml` - Main production configuration
- `docker-compose.override.yml` - Development overrides (automatically applied)
- `.env.example` - Environment variables template

### Dockerfiles
- `backend/Dockerfile` - Production backend
- `backend/Dockerfile.dev` - Development backend with hot reload
- `frontend/Dockerfile` - Production frontend (multi-stage build)
- `frontend/Dockerfile.dev` - Development frontend with hot reload

## Usage

### Development
```bash
# Start development environment
docker-compose up

# Start with rebuild
docker-compose up --build

# Stop services
docker-compose down
```

### Production
```bash
# Start production environment
docker-compose --profile production up

# Production with detached mode
docker-compose --profile production up -d

# Stop production
docker-compose --profile production down
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

### Required Variables
- `JWT_SECRET_KEY` - JWT signing secret
- `SESSION_SECRET` - Session encryption key
- `ENCRYPTION_KEY` - Data encryption key
- `API_SECRET_KEY` - API authentication key

### Optional Variables
- `ENVIRONMENT` - development/production (default: development)
- `DEBUG` - Debug mode (default: true)
- `RATE_LIMIT_ENABLED` - Enable rate limiting (default: true)
- `NEXT_PUBLIC_API_URL` - Frontend API URL

## Services

### Backend
- **Port**: 8001
- **Health Check**: `/api/health`
- **Hot Reload**: Enabled in development

### Frontend
- **Port**: 3000
- **Health Check**: HTTP 200 on root
- **Hot Reload**: Enabled in development

### Redis
- **Port**: 6379
- **Health Check**: `redis-cli ping`

### Nginx (Production Only)
- **Ports**: 80, 443
- **Profile**: production
- **SSL**: Configure in `nginx/ssl/`

## Networks
- `atp-network`: Bridge network with subnet 172.20.0.0/16
- All services communicate internally through this network

## Volumes
- `redis_data`: Redis persistent data
- `redis_dev_data`: Development Redis data (override)

## Migration from Old Structure

### Files to Remove
- `docker-compose.dev.yml`
- `docker-compose.prod.yml`
- `docker-compose.production.yml`
- `docker-compose.simple.yml`
- `scripts/docker-compose.secrets.yml`

### Migration Steps
1. Copy `.env.example` to `.env` and update secrets
2. Replace old `docker-compose.yml` with new version
3. Update any scripts referencing old compose files
4. Test with `docker-compose up --build`

## Benefits of New Structure

1. **Simplified**: Single main compose file with override for development
2. **Consistent**: Standardized naming and versions
3. **Flexible**: Environment-based configuration
4. **Secure**: Proper secret management
5. **Maintainable**: Clear separation of concerns

## Troubleshooting

### Port Conflicts
Ensure ports 3000, 8001, 6379, 80, 443 are available

### Environment Issues
Check `.env` file exists and variables are properly set

### Build Problems
Use `docker-compose up --build` to rebuild images

### Health Check Failures
Verify services are running and accessible internally
