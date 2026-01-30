# ATP Platform v0.8.0 - DuckDNS Deployment Guide
## Ubuntu 24.04 VPS (NiceTry) - http://atp-app.duckdns.org

### 🚀 Quick Deploy with Custom Domain

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

# 4. Set production environment with custom domain
cp .env.production .env

# 5. Deploy with custom domain
docker-compose -f docker-compose.prod.yml up -d --build

# 6. Verify
curl http://atp-app.duckdns.org:3000
curl http://atp-app.duckdns.org:8001/api/health
```

---

### 🔧 Environment Configuration (.env)

```bash
# Frontend
NEXT_PUBLIC_API_URL=http://atp-app.duckdns.org:8001
NODE_ENV=production

# Backend
API_HOST=0.0.0.0
API_PORT=8001
REDIS_HOST=redis
REDIS_PORT=6379

# CORS for custom domain
CORS_ORIGINS=http://atp-app.duckdns.org:3000,http://localhost:3000
```

---

### 🌐 Access URLs

- **Frontend**: http://atp-app.duckdns.org:3000
- **Backend API**: http://atp-app.duckdns.org:8001
- **Health Check**: http://atp-app.duckdns.org:8001/api/health
- **WebSocket**: ws://atp-app.duckdns.org:8001/ws

---

### 📋 Ports & Firewall

```bash
# Open ports for custom domain
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8001/tcp  # Backend API
sudo ufw allow 6379/tcp  # Redis (internal)
sudo ufw enable
```

---

### 🛠️ DuckDNS Setup (Already Done)

✅ **Domain**: atp-app.duckdns.org  
✅ **Token**: ba7dde1a-668b-42dc-a6b6-9a40fde892df  
✅ **Account**: ezequielalonso121@gmail.com  
✅ **Status**: Active (2 weeks old)

---

### 🔍 Health Checks

```bash
# Frontend
curl -I http://atp-app.duckdns.org:3000

# Backend Health
curl http://atp-app.duckdns.org:8001/api/health

# Docker Status
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

---

### 🚨 Troubleshooting

**Domain not resolving:**
```bash
# Check DNS
nslookup atp-app.duckdns.org
ping atp-app.duckdns.org
```

**CORS errors:**
```bash
# Verify CORS origins include your domain
docker-compose logs backend | grep CORS
```

**Frontend not loading:**
```bash
# Check NEXT_PUBLIC_API_URL matches backend domain
docker-compose logs frontend
```

---

### 🎯 Production Features

- ✅ Custom domain: atp-app.duckdns.org
- ✅ Multi-user storage system
- ✅ 30 AI agents ready
- ✅ 10 themes with improved contrast
- ✅ Professional agent name formatting
- ✅ WebSocket real-time chat
- ✅ CORS configured for custom domain
- ✅ Production environment variables

---

### 📊 Optional HTTPS Setup

```bash
# Install certbot for HTTPS
sudo apt install certbot python3-certbot-nginx

# Get certificate for custom domain
sudo certbot --nginx -d atp-app.duckdns.org

# Auto-renew
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

### 🎉 Launch Ready!

Your ATP Platform is now configured with custom domain access:

**Main URL**: http://atp-app.duckdns.org:3000

Deploy now and test all features! 🚀
