@echo off
REM AFW Deployment Script for Windows
REM This script deploys the AFW project with unique ports and configuration

echo.
echo ========================================
echo    AFW Deployment Script
echo ========================================
echo.

REM Stop any existing AFW containers
echo Stopping existing AFW containers...
docker-compose -f docker-compose.afw.yml down 2>nul

REM Remove old AFW containers if they exist
echo Cleaning up old containers...
docker rm -f afw-backend afw-frontend afw-redis 2>nul

REM Prune unused networks
echo Cleaning up networks...
docker network prune -f

REM Build and start AFW services
echo Building and starting AFW services...
docker-compose -f docker-compose.afw.yml --env-file .env.afw up -d --build

REM Wait for services to be healthy
echo Waiting for services to be healthy...
timeout /t 15 /nobreak >nul

REM Check service status
echo.
echo Checking service status...
docker-compose -f docker-compose.afw.yml ps

echo.
echo ========================================
echo    AFW Deployment Complete!
echo ========================================
echo.
echo Services running on:
echo    - Frontend: http://localhost:3002
echo    - Backend:  http://localhost:8002
echo    - Redis:    localhost:6380
echo.
echo Public URL: http://afw-app.duckdns.org
echo.
pause
