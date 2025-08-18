#!/bin/bash

# 🚀 Запуск AI Tutor Server
echo "🚀 Запуск AI Tutor Server"
echo ""

# Проверка Docker
echo "📋 Проверка Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker"
    exit 1
fi

docker --version
echo "✅ Docker найден"

echo ""
echo "📝 Создание .env файла..."

# Создание .env файла
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ .env файл создан из env.example"
    echo "⚠️  Не забудьте настроить OPENAI_API_KEY в .env файле!"
else
    echo "✅ .env файл уже существует"
fi

echo ""
echo "🐳 Запуск сервисов..."

# Запуск Docker Compose
docker compose up --build 