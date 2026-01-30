# 🔐 ATP Security Implementation v1.1.0

## Mejoras de Seguridad Implementadas

### 1. **Rate Limiting & DDoS Protection** ✅

**Archivo**: `backend/app/security/rate_limiter.py`

**Características**:
- ✅ Límite de 60 requests/minuto por IP
- ✅ Límite de 1000 requests/hora por IP
- ✅ Bloqueo automático de IPs abusivas (1 hora)
- ✅ Detección de X-Forwarded-For para proxies
- ✅ Registro de intentos fallidos
- ✅ Limpieza automática de ventanas antiguas

**Configuración**:
```python
max_requests_per_minute = 60
max_requests_per_hour = 1000
max_failed_attempts = 10
block_duration = 3600  # 1 hora
```

---

### 2. **Autenticación Admin Robusta** ✅

**Archivo**: `backend/app/security/admin_auth.py`

**Características**:
- ✅ Usuario y contraseña generados automáticamente
- ✅ Contraseña de 32 caracteres (letras, números, símbolos)
- ✅ Hash PBKDF2-HMAC-SHA256 con 100,000 iteraciones
- ✅ Tokens de sesión con expiración (1 hora)
- ✅ Comparación segura con `hmac.compare_digest`
- ✅ Log de intentos de acceso

**Credenciales**:
```
Username: admin_<16_hex_chars>
Password: <32_secure_chars>
```

**Uso**:
```python
# Proteger ruta admin
@app.get("/admin/dashboard")
async def admin_dashboard(auth=Depends(admin_auth.require_admin)):
    return {"status": "authenticated"}
```

---

### 3. **Protección Anti-Scraping** ✅

**Archivo**: `backend/app/security/anti_scraping.py`

**Características**:
- ✅ Detección de User-Agents sospechosos (bots, crawlers)
- ✅ Verificación de headers requeridos
- ✅ Fingerprinting de requests
- ✅ Detección de comportamiento automatizado
- ✅ Análisis de patrones de intervalos regulares
- ✅ Bloqueo de >30 requests/minuto

**Patrones Bloqueados**:
```
bot, crawler, spider, scraper, curl, wget,
python-requests, scrapy, selenium, phantomjs
```

**Headers Requeridos**:
```
- user-agent
- accept
- accept-language
```

---

### 4. **CORS Restrictivo & Security Headers** ✅

**Archivo**: `backend/app/security/cors_config.py`

**Orígenes Permitidos**:
```python
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://atp-app.duckdns.org",
]
```

**Security Headers**:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: [restrictive policy]
```

---

## Integración en Backend

### Paso 1: Importar Módulos de Seguridad

```python
from app.security import (
    rate_limiter,
    admin_auth,
    anti_scraping,
    configure_cors
)
```

### Paso 2: Configurar Middleware

```python
# CORS restrictivo
configure_cors(app)

# Rate limiting
app.middleware("http")(rate_limiter)

# Anti-scraping
app.middleware("http")(anti_scraping)
```

### Paso 3: Proteger Rutas Admin

```python
@app.get("/admin/dashboard", dependencies=[Depends(admin_auth.require_admin)])
async def admin_dashboard():
    return {"status": "ok"}

@app.post("/admin/login")
async def admin_login(credentials: HTTPBasicCredentials = Depends(security)):
    token = admin_auth.authenticate(credentials)
    return {"token": token}
```

---

## Mejoras de UI Implementadas

### 1. **Botones Móviles Optimizados** ✅
- Posición: `bottom-0` (sin obstruir chat)
- Tamaño: Iconos `w-5 h-5`, texto `text-[10px]`
- Menú hamburguesa removido

### 2. **Selección de Tareas Funcional** ✅
- Al seleccionar tarea, activa automáticamente los 5 agentes
- Muestra agentes especializados en cada tarea
- Cierra panel automáticamente

### 3. **Botón Memoria Conectado** ✅
- Abre `ConversationSidebar` con historial
- Permite crear nueva conversación
- Cierra automáticamente al seleccionar

---

## Configuración de Producción

### Variables de Entorno

```bash
# Admin Credentials (opcional - se generan automáticamente)
ADMIN_USERNAME=admin_<custom>
ADMIN_PASSWORD_HASH=<pbkdf2_hash>

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_REQUESTS_PER_HOUR=1000

# CORS
ALLOWED_ORIGINS=https://atp-app.duckdns.org,http://localhost:3000
```

### Obtener Credenciales Admin

Al iniciar el backend por primera vez, verás:

```
============================================================
ADMIN CREDENTIALS GENERATED
============================================================
Username: admin_a1b2c3d4e5f6g7h8
Password: xYz123_AbC456-DeF789_GhI012
============================================================
SAVE THESE CREDENTIALS SECURELY!
============================================================
```

**⚠️ IMPORTANTE**: Guarda estas credenciales en un lugar seguro.

---

## Testing de Seguridad

### Test 1: Rate Limiting

```bash
# Enviar 100 requests rápidas
for i in {1..100}; do
  curl http://localhost:8001/api/health
done

# Resultado esperado: HTTP 429 después de 60 requests
```

### Test 2: Anti-Scraping

```bash
# Request con User-Agent de bot
curl -H "User-Agent: python-requests/2.28.0" http://localhost:8001/api/chat

# Resultado esperado: HTTP 403 Forbidden
```

### Test 3: Admin Auth

```bash
# Login admin
curl -X POST http://localhost:8001/admin/login \
  -u "admin_xxx:password_xxx"

# Resultado esperado: {"token": "..."}

# Acceder a dashboard
curl -H "Authorization: Bearer <token>" \
  http://localhost:8001/admin/dashboard

# Resultado esperado: {"status": "authenticated"}
```

### Test 4: CORS

```bash
# Request desde origen no permitido
curl -H "Origin: https://malicious-site.com" \
  http://localhost:8001/api/health

# Resultado esperado: CORS error
```

---

## Monitoreo y Logs

### Ver IPs Bloqueadas

```python
from app.security import rate_limiter

# Ver IPs bloqueadas
print(rate_limiter.blocked_ips)

# Ver intentos fallidos
print(rate_limiter.failed_attempts)
```

### Ver IPs Sospechosas (Scraping)

```python
from app.security import anti_scraping

# Ver IPs sospechosas
print(anti_scraping.suspicious_ips)
```

---

## Recomendaciones Adicionales

### 1. **Firewall & Nginx**
```nginx
# Rate limiting en Nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend:8001;
}
```

### 2. **Fail2Ban**
```ini
[atp-api]
enabled = true
port = 8001
filter = atp-api
logpath = /var/log/atp/access.log
maxretry = 10
bantime = 3600
```

### 3. **SSL/TLS**
```bash
# Usar Let's Encrypt
certbot --nginx -d atp-app.duckdns.org
```

### 4. **Backup de Credenciales**
```bash
# Guardar en archivo seguro
echo "ADMIN_USERNAME=admin_xxx" > .env.admin
echo "ADMIN_PASSWORD_HASH=xxx" >> .env.admin
chmod 600 .env.admin
```

---

## Checklist de Seguridad

- [x] Rate limiting implementado
- [x] Admin auth con credenciales robustas
- [x] Anti-scraping activo
- [x] CORS restrictivo configurado
- [x] Security headers agregados
- [x] Rutas admin protegidas
- [ ] SSL/TLS en producción
- [ ] Firewall configurado
- [ ] Fail2Ban activo
- [ ] Backups automáticos
- [ ] Monitoreo de logs
- [ ] Alertas de seguridad

---

## Contacto de Seguridad

Para reportar vulnerabilidades:
- Email: security@atp-app.duckdns.org
- Respuesta en: 24-48 horas

---

**ATP v1.1.0 - Sistema de Seguridad Robusto** 🔐
