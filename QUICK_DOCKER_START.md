# 🚀 Inicio Rápido con Docker

## Comandos para Correr ATP Localmente

### 1. Preparar el Entorno

```bash
# Crear archivo .env desde el ejemplo
cp .env.example .env

# Crear directorios necesarios
mkdir -p backend/data
mkdir -p logs
```

### 2. Iniciar Todo el Sistema

```bash
# Construir y levantar todos los servicios
docker-compose -f docker-compose.dev.yml up --build
```

### 3. Acceder a la Aplicación

🌐 **Frontend**: http://localhost:3000  
🔧 **Backend API**: http://localhost:8001  
📚 **API Docs**: http://localhost:8001/docs  
📊 **Admin Dashboard**: http://localhost:8001/admin/dashboard  

### 4. Verificar Funcionamiento

```bash
# En otra terminal, verificar health
curl http://localhost:8001/api/health

# Ver logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 📱 Funcionalidades Disponibles

✅ **Historial de Conversaciones** - Sidebar estilo ChatGPT  
✅ **Guardar Respuestas** - Botón 💾 en cada respuesta de agente  
✅ **Biblioteca de Respuestas** - Biblioteca con búsqueda y categorías  
✅ **Interfaz Móvil** - Texto legible y optimizado  
✅ **Monitoreo Admin** - Dashboard en tiempo real  
✅ **REST API** - Para integraciones externas  
✅ **Usuarios Online** - Tracking en tiempo real con Redis  

---

## 🔧 Comandos Útiles

```bash
# Detener todo
docker-compose -f docker-compose.dev.yml down

# Reiniciar un servicio
docker-compose -f docker-compose.dev.yml restart backend

# Ver logs de un servicio
docker-compose -f docker-compose.dev.yml logs -f frontend

# Entrar al contenedor backend
docker-compose -f docker-compose.dev.yml exec backend bash

# Limpiar y reconstruir todo
docker-compose -f docker-compose.dev.yml down
docker system prune -f
docker-compose -f docker-compose.dev.yml up --build
```

---

## 🐛 Si Algo Falla

### Puerto en uso
```bash
# Cambiar puertos en docker-compose.dev.yml
ports:
  - "8002:8001"  # Backend
  - "3001:3000"  # Frontend
```

### Permisos (Linux/Mac)
```bash
sudo chown -R $USER:$USER backend/data
chmod 755 backend/data
```

### Verificar estado
```bash
docker-compose -f docker-compose.dev.yml ps
docker stats
```

---

**¡Listo! La aplicación ATP está corriendo localmente con todas las funcionalidades.** 🎉
