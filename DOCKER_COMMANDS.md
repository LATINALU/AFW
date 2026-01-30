# 🐳 Docker Commands - ATP Management

## 📋 Scripts Disponibles

### 🚀 Iniciar ATP
**Windows**: `.\RUN_DOCKER.bat`  
**Linux/Mac**: `./RUN_DOCKER.sh`

Construye e inicia todos los servicios con las nuevas funcionalidades.

### 🛑 Detener ATP
**Windows**: `.\STOP_DOCKER.bat`  
**Linux/Mac**: `./STOP_DOCKER.sh`

Detiene los servicios y limpía contenedores.

### 🔄 Resetear ATP
**Windows**: `.\RESET_DOCKER.bat`  
**Linux/Mac**: `./RESET_DOCKER.sh`

Restructura completa: elimina contenedores, imágenes y vuelve a construir desde cero.

---

## 🔧 Comandos Manuales

### Básicos
```bash
# Iniciar todo
docker-compose -f docker-compose.dev.yml up --build

# Iniciar en background
docker-compose -f docker-compose.dev.yml up -d --build

# Detener todo
docker-compose -f docker-compose.dev.yml down

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Mantenimiento
```bash
# Ver estado de contenedores
docker-compose -f docker-compose.dev.yml ps

# Ver recursos usados
docker stats

# Reiniciar un servicio específico
docker-compose -f docker-compose.dev.yml restart backend

# Entrar a contenedor
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec frontend sh
```

### Limpieza
```bash
# Limpiar contenedores huérfanos
docker container prune -f

# Limpiar imágenes no usadas
docker image prune -f

# Limpiar volúmenes no usados (CUIDADO)
docker volume prune -f

# Limpieza completa del sistema
docker system prune -af
```

### Reconstrucción
```bash
# Reconstruir solo imágenes
docker-compose -f docker-compose.dev.yml build

# Reconstruir desde cero
docker-compose -f docker-compose.dev.yml down --rmi all
docker-compose -f docker-compose.dev.yml up --build

# Forzar recreación de contenedores
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

---

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. "Port already in use"
```bash
# Ver qué usa el puerto
netstat -tulpn | grep :8001
lsof -i :8001

# Matar proceso
kill -9 <PID>

# O usar diferentes puertos en docker-compose.dev.yml
```

#### 2. "Build failed"
```bash
# Limpiar y reconstruir
docker-compose -f docker-compose.dev.yml down
docker system prune -f
docker-compose -f docker-compose.dev.yml up --build
```

#### 3. "Database locked"
```bash
# Reiniciar backend
docker-compose -f docker-compose.dev.yml restart backend

# O resetear completo
./RESET_DOCKER.sh
```

#### 4. "Redis connection failed"
```bash
# Verificar Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli ping

# Reiniciar Redis
docker-compose -f docker-compose.dev.yml restart redis
```

#### 5. "Permission denied" (Linux/Mac)
```bash
# Permisos de directorios
sudo chown -R $USER:$USER backend/data
chmod 755 backend/data
chmod +x *.sh
```

### Verificación

```bash
# Health check
curl http://localhost:8001/api/health

# Verificar servicios
docker-compose -f docker-compose.dev.yml ps

# Ver logs de errores
docker-compose -f docker-compose.dev.yml logs backend | grep ERROR
```

---

## 📊 Monitoreo

### Recursos
```bash
# Estadísticas en tiempo real
docker stats

# Uso de disco
docker-compose -f docker-compose.dev.yml exec backend df -h

# Memoria Redis
docker-compose -f docker-compose.dev.yml exec redis redis-cli info memory
```

### Logs
```bash
# Logs con timestamps
docker-compose -f docker-compose.dev.yml logs -f --timestamps

# Logs específicos
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend
docker-compose -f docker-compose.dev.yml logs -f redis
```

---

## 🔄 Flujo de Desarrollo

### 1. Inicio del Día
```bash
# Iniciar todo
./RUN_DOCKER.sh

# O si ya existe, solo iniciar
docker-compose -f docker-compose.dev.yml up -d
```

### 2. Durante Desarrollo
```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Reiniciar si hay cambios
docker-compose -f docker-compose.dev.yml restart backend

# Reconstruir si hay cambios en Dockerfile
docker-compose -f docker-compose.dev.yml build backend
```

### 3. Fin del Día
```bash
# Detener todo
./STOP_DOCKER.sh

# O dejar corriendo para mañana
# (no hacer nada, sigue corriendo)
```

### 4. Reset Completo (si algo falla)
```bash
# Reset completo
./RESET_DOCKER.sh
```

---

## 🎯 Acceso Rápido

Una vez iniciado, accede a:

- **🌐 Frontend**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8001
- **📚 API Docs**: http://localhost:8001/docs
- **📊 Admin Dashboard**: http://localhost:8001/admin/dashboard
- **👥 Users Online**: http://localhost:8001/api/admin/stats/online-users
- **💾 Conversaciones**: http://localhost:8001/api/conversations/list

---

## 📱 Funcionalidades Disponibles

✅ **Historial de Conversaciones** - Sidebar estilo ChatGPT  
✅ **Guardar Respuestas** - Botón 💾 en cada respuesta  
✅ **Biblioteca de Respuestas** - Con búsqueda y categorías  
✅ **Interfaz Móvil** - Texto legible y optimizado  
✅ **Admin Dashboard** - Monitoreo en tiempo real  
✅ **REST API** - Para integraciones externas  
✅ **Usuarios Online** - Tracking con Redis  
✅ **Rate Limiting** - Protección contra sobrecarga  

---

**¡Listo para desarrollar con ATP en Docker!** 🚀
