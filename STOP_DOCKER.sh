#!/bin/bash

echo "🛑 Deteniendo ATP Docker..."
echo

# Detener y eliminar contenedores
docker-compose -f docker-compose.dev.yml down

# Eliminar contenedores huérfanos
docker container prune -f

# Limpiar imágenes no usadas (opcional)
echo "Limpiando imágenes no usadas..."
docker image prune -f

# Limpiar volúmenes no usados (opcional - CUIDADO: elimina datos)
read -p "¿Deseas limpiar volúmenes? (S/N): " clean_volumes
if [[ $clean_volumes =~ ^[Ss]$ ]]; then
    echo "Eliminando volúmenes no usados..."
    docker volume prune -f
fi

echo
echo "✅ Docker detenido y limpiado!"
echo
echo "Para volver a iniciar:"
echo "./RUN_DOCKER.sh"
