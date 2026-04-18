@echo off
echo Workday Automation Tool - Windows Installation
echo =============================================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating configuration file...
if not exist config.json (
    copy config\config_template.json config.json
    echo Configuration file created: config.json
    echo Please edit config.json with your credentials and job URLs
) else (
    echo Configuration file already exists
)

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Edit config.json with your credentials
echo 2. Add job URLs to the configuration
echo 3. Run: python run.py
echo.
pause
