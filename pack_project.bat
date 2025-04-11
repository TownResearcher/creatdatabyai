@echo off
echo Starting project backup...

REM Create backup directory
mkdir project_backup
cd project_backup

REM Copy core files
echo Copying core files...
xcopy /Y ..\main.py .
xcopy /Y ..\requirements.txt .
xcopy /Y ..\Dockerfile .
xcopy /Y ..\docker-compose.yml .
xcopy /Y ..\.env .

REM Copy config files
echo Copying config files...
xcopy /Y ..\.dockerignore .
xcopy /Y ..\.gitignore .

REM Copy documentation
echo Copying documentation...
xcopy /Y ..\*.md .

REM Copy data files
echo Copying data files...
xcopy /Y "..\No.001 姻缘.txt" .

REM Export Docker image
echo Exporting Docker image...
docker save creatdatabyai-app > creatdatabyai-app.tar

echo Backup completed!
echo Project files have been saved to project_backup directory
pause 