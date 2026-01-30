@echo off
echo 🛑 Deteniendo ATP Docker...
echo.

REM Detener y eliminar contenedores
docker-compose -f docker-compose.dev.yml down

REM Eliminar contenedores huérfanos
docker container prune -f

REM Limpiar imágenes no usadas (opcional)
echo Limpiando imágenes no usadas...
docker image prune -f

REM Limpiar volúmenes no usados (opcional - CUIDADO: elimina datos)
echo ¿Deseas limpiar volúmenes? (S/N)
set /p clean_volumes=
if /i "%clean_volumes%"=="S" (
    echo Eliminando volúmenes no usados...
    docker volume prune -f
)

echo.
echo ✅ Docker detenido y limpiado!
echo.
echo Para volver a iniciar:
echo .\RUN_DOCKER.bat
pause
