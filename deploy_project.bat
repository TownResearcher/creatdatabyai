@echo off
echo Starting project deployment...

REM Check if Docker is installed
docker --version
if errorlevel 1 (
    echo Error: Docker is not installed! Please install Docker Desktop first.
    pause
    exit /b
)

REM Import Docker image if exists
if exist creatdatabyai-app.tar (
    echo Importing Docker image...
    docker load < creatdatabyai-app.tar
)

REM Build and start container
echo Building and starting container...
docker-compose up --build -d

echo Deployment completed!
echo Please visit http://localhost:8000 to check if the application is running
pause 