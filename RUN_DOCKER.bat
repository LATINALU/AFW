@echo off
echo 🚀 Iniciando ATP con Docker...
echo.

REM Crear directorios necesarios
if not exist "backend\data" mkdir backend\data
if not exist "logs" mkdir logs

REM Crear archivo .env si no existe
if not exist ".env" (
    echo Creando archivo .env desde .env.example...
    copy .env.example .env
)

echo Construyendo e iniciando servicios...
echo Esto puede tomar varios minutos la primera vez...
echo.

REM Iniciar Docker Compose
docker-compose -f docker-compose.dev.yml up --build

echo.
echo ✅ ATP está corriendo!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8001
echo 📚 API Docs: http://localhost:8001/docs
echo 📊 Admin Dashboard: http://localhost:8001/admin/dashboard
echo.
echo Presiona Ctrl+C para detener los servicios.
pause
