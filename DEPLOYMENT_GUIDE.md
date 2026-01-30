# ATP Platform v0.8.0 - Deployment Guide
## Ubuntu 24.04 VPS (NiceTry) - 147.93.191.92

### 🚀 Quick Deploy (Docker Compose)

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Docker & Docker Compose
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# 3. Clone repo
git clone https://github.com/LATINALU/ATPE.git
cd ATPE

# 4. Set production environment
cp .env.example .env
nano .env  # Edit as needed (see below)

# 5. Deploy
docker-compose up -d --build

# 6. Verify
curl http://147.93.191.92:3000
curl http://147.93.191.92:8001/api/health
```

---

### 🔧 Environment Variables (.env)

```bash
# Frontend
NEXT_PUBLIC_API_URL=http://147.93.191.92:8001
NODE_ENV=production

# Backend
API_HOST=0.0.0.0
API_PORT=8001
REDIS_HOST=redis
REDIS_PORT=6379

# Optional: API Keys (for users to configure)
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

---

### 📋 Ports & Firewall

```bash
# Open ports (if UFW active)
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8001/tcp  # Backend API
sudo ufw allow 6379/tcp  # Redis (internal only)
sudo ufw enable
```

---

### 🐳 Docker Compose Production

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://147.93.191.92:8001
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8001
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

---

### 🔍 Health Checks

```bash
# Frontend
curl -I http://147.93.191.92:3000

# Backend Health
curl http://147.93.191.92:8001/api/health

# Docker Status
docker-compose ps
docker-compose logs -f
```

---

### 🛠️ Troubleshooting

**Frontend not loading:**
```bash
docker-compose logs frontend
# Check NEXT_PUBLIC_API_URL matches backend IP:port
```

**Backend not responding:**
```bash
docker-compose logs backend
# Verify API_HOST=0.0.0.0 and API_PORT=8001
```

**Redis connection:**
```bash
docker-compose exec redis redis-cli ping
```

---

### 🌐 Optional HTTPS (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Auto-renew
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

### 📊 Production Optimizations

- Set `NODE_ENV=production`
- Use Redis persistence if needed
- Configure reverse proxy (nginx) for SSL
- Monitor with `docker stats`
- Backup Redis data: `docker exec redis redis-cli BGSAVE`

---

### 🎯 Access URLs

- **Frontend**: http://147.93.191.92:3000
- **Backend API**: http://147.93.191.92:8001
- **Health Check**: http://147.93.191.92:8001/api/health

---

### 📝 Notes

- Platform supports 30 AI agents
- Multi-user storage via localStorage (anonymous users)
- 10 themes with improved contrast
- WebSocket on port 8001
- No authentication required for demo mode

Deploy complete! 🚀
