@echo off
echo Syncing code changes...

REM Pull latest changes
echo Pulling latest changes...
git pull origin master

REM Add all changes
echo Adding changes...
git add .

REM Commit changes
echo Enter commit message:
set /p COMMIT_MSG=
git commit -m "%COMMIT_MSG%"

REM Push changes
echo Pushing changes...
git push origin master

REM Rebuild and restart Docker containers
echo Rebuilding and restarting Docker containers...
docker-compose down
docker-compose up --build -d

echo Sync completed!
pause 