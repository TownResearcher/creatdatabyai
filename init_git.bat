@echo off
echo Initializing Git repository...

REM Initialize Git repository
git init

REM Add all files
git add .

REM Initial commit
git commit -m "Initial commit"

REM Add remote repository
git remote add origin https://github.com/TownResearcher/creatdatabyai.git

REM Push to remote
git push -u origin master

echo Git repository initialized and code pushed!
pause 