@echo off
echo Syncing code changes...

REM 检查本地是否有未提交的更改
echo Checking for local changes...
git status | findstr /C:"Changes not staged for commit:" > nul
if errorlevel 1 (
    echo No local changes detected, proceeding with pull...
    goto pull_changes
) else (
    echo Local changes detected, proceeding with push...
    goto push_changes
)

:pull_changes
REM Pull latest changes
echo Pulling latest changes...
git pull origin master
if errorlevel 1 (
    echo [ERROR] Failed to pull changes
    pause
    exit /b 1
)
echo Pull successful!
goto end

:push_changes
REM Add all changes
echo Adding changes...
git add .
if errorlevel 1 (
    echo [ERROR] Failed to add changes
    pause
    exit /b 1
)

REM Commit changes
echo Enter commit message:
set /p COMMIT_MSG=
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [ERROR] Failed to commit changes
    pause
    exit /b 1
)

REM Push changes
echo Pushing changes...
git push origin master
if errorlevel 1 (
    echo [ERROR] Failed to push changes
    pause
    exit /b 1
)

REM Rebuild and restart Docker containers
echo Rebuilding and restarting Docker containers...
docker-compose down
if errorlevel 1 (
    echo [ERROR] Failed to stop Docker containers
    pause
    exit /b 1
)

docker-compose up --build -d
if errorlevel 1 (
    echo [ERROR] Failed to start Docker containers
    pause
    exit /b 1
)

:end
echo Sync completed!
pause 