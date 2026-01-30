#!/bin/bash

echo "🚀 Iniciando ATP con Docker..."
echo

# Crear directorios necesarios
mkdir -p backend/data
mkdir -p logs

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env desde .env.example..."
    cp .env.example .env
fi

echo "Construyendo e iniciando servicios..."
echo "Esto puede tomar varios minutos la primera vez..."
echo

# Iniciar Docker Compose
docker-compose -f docker-compose.dev.yml up --build

echo
echo "✅ ATP está corriendo!"
echo
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo "📊 Admin Dashboard: http://localhost:8001/admin/dashboard"
echo
echo "Presiona Ctrl+C para detener los servicios."
