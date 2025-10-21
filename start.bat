@echo off
echo 🔍 Crypto Price Detector
echo ========================
echo.

echo Проверка Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.7+
    pause
    exit /b 1
)

echo.
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Запуск приложения...
python run_app.py

pause
