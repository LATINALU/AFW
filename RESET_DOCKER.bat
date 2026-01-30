@echo off
echo 🔄 Reseteando ATP Docker - Restructuración Completa...
echo.

REM Paso 1: Detener todo
echo [1/5] Deteniendo contenedores...
docker-compose -f docker-compose.dev.yml down

REM Paso 2: Eliminar contenedores
echo [2/5] Eliminando contenedores...
docker-compose -f docker-compose.dev.yml down --remove-orphans

REM Paso 3: Limpiar imágenes del proyecto
echo [3/5] Eliminando imágenes del proyecto...
docker-compose -f docker-compose.dev.yml down --rmi all

REM Paso 4: Limpiar sistema (opcional pero recomendado)
echo [4/5] Limpiando sistema Docker...
docker system prune -f

REM Paso 5: Limpiar volúmenes (CUIDADO - elimina datos)
echo [5/5] ¿Deseas eliminar volúmenes? (S/N) - ¡Esto eliminará todos los datos!
set /p clean_volumes=
if /i "%clean_volumes%"=="S" (
    echo Eliminando volúmenes...
    docker volume prune -f
    docker-compose -f docker-compose.dev.yml down -v
)

echo.
echo ✅ Reseteo completo finalizado!
echo.

REM Recrear directorios
if not exist "backend\data" mkdir backend\data
if not exist "logs" mkdir logs

echo 🚀 Iniciando ATP con estructura limpia...
echo.

REM Iniciar todo desde cero
docker-compose -f docker-compose.dev.yml up --build

echo.
echo ✅ ATP reestructurado y corriendo!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8001
echo 📚 API Docs: http://localhost:8001/docs
echo 📊 Admin: http://localhost:8001/admin/dashboard
pause
