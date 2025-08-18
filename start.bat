@echo off
echo 🚀 Запуск AI Tutor Server
echo.

echo 📋 Проверка Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен. Установите Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker найден

echo.
echo 📝 Создание .env файла...
if not exist .env (
    copy env.example .env
    echo ✅ .env файл создан из env.example
    echo ⚠️  Не забудьте настроить OPENAI_API_KEY в .env файле!
) else (
    echo ✅ .env файл уже существует
)

echo.
echo 🐳 Запуск сервисов...
docker compose up --build

pause 