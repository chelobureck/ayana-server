# 🚀 Запуск AI Tutor Server
Write-Host "🚀 Запуск AI Tutor Server" -ForegroundColor Green
Write-Host ""

# Проверка Docker
Write-Host "📋 Проверка Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker найден: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker не установлен. Установите Docker Desktop" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host ""
Write-Host "📝 Создание .env файла..." -ForegroundColor Yellow

# Создание .env файла
if (-not (Test-Path ".env")) {
    Copy-Item "env.example" ".env"
    Write-Host "✅ .env файл создан из env.example" -ForegroundColor Green
    Write-Host "⚠️  Не забудьте настроить OPENAI_API_KEY в .env файле!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env файл уже существует" -ForegroundColor Green
}

Write-Host ""
Write-Host "🐳 Запуск сервисов..." -ForegroundColor Yellow

# Запуск Docker Compose
docker compose up --build

Read-Host "Нажмите Enter для выхода" 