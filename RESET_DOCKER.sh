#!/bin/bash

echo "🔄 Reseteando ATP Docker - Restructuración Completa..."
echo

# Paso 1: Detener todo
echo "[1/5] Deteniendo contenedores..."
docker-compose -f docker-compose.dev.yml down

# Paso 2: Eliminar contenedores
echo "[2/5] Eliminando contenedores..."
docker-compose -f docker-compose.dev.yml down --remove-orphans

# Paso 3: Limpiar imágenes del proyecto
echo "[3/5] Eliminando imágenes del proyecto..."
docker-compose -f docker-compose.dev.yml down --rmi all

# Paso 4: Limpiar sistema (opcional pero recomendado)
echo "[4/5] Limpiando sistema Docker..."
docker system prune -f

# Paso 5: Limpiar volúmenes (CUIDADO - elimina datos)
echo "[5/5] ¿Deseas eliminar volúmenes? (S/N) - ¡Esto eliminará todos los datos!"
read -p "Respuesta: " clean_volumes
if [[ $clean_volumes =~ ^[Ss]$ ]]; then
    echo "Eliminando volúmenes..."
    docker volume prune -f
    docker-compose -f docker-compose.dev.yml down -v
fi

echo
echo "✅ Reseteo completo finalizado!"
echo

# Recrear directorios
mkdir -p backend/data
mkdir -p logs

echo "🚀 Iniciando ATP con estructura limpia..."
echo

# Iniciar todo desde cero
docker-compose -f docker-compose.dev.yml up --build

echo
echo "✅ ATP reestructurado y corriendo!"
echo
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo "📊 Admin: http://localhost:8001/admin/dashboard"
