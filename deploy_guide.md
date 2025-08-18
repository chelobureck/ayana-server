# 🚀 Руководство по деплою AI Tutor Server

## 🌐 Render (Рекомендуется для MVP)

### 1. Подготовка репозитория
```bash
# Убедитесь что все файлы закоммичены
git add .
git commit -m "Initial AI Tutor Server setup"
git push origin main
```

### 2. Создание аккаунта на Render
- Зайдите на [render.com](https://render.com)
- Создайте аккаунт (можно через GitHub)
- Подключите ваш репозиторий

### 3. Создание Web Service
1. **New → Web Service**
2. **Connect Repository** → выберите ваш репозиторий
3. **Name**: `ai-tutor-api`
4. **Environment**: `Docker`
5. **Region**: выберите ближайший
6. **Branch**: `main`
7. **Root Directory**: оставьте пустым

### 4. Настройка переменных окружения
В разделе **Environment Variables** добавьте:

```bash
# Обязательные
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# База данных (создадим позже)
DB_HOST=${DATABASE_INTERNAL_HOST}
DB_PORT=${DATABASE_INTERNAL_PORT}
DB_USER=${DATABASE_USER}
DB_PASSWORD=${DATABASE_PASSWORD}
DB_NAME=${DATABASE_NAME}

# Redis (создадим позже)
REDIS_HOST=${REDIS_HOST}
REDIS_PORT=${REDIS_PORT}
REDIS_DB=0

# Безопасность
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_ALG=HS256

# CORS
APP_CORS_ORIGINS=*
```

### 5. Создание PostgreSQL базы данных
1. **New → PostgreSQL**
2. **Name**: `ai-tutor-db`
3. **Database**: `aitutor`
4. **User**: `aitutor_user`
5. **Region**: тот же что и для API

После создания скопируйте переменные в Web Service:
- `DATABASE_INTERNAL_HOST`
- `DATABASE_INTERNAL_PORT`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_NAME`

### 6. Создание Redis
1. **New → Redis**
2. **Name**: `ai-tutor-redis`
3. **Region**: тот же что и для API

Скопируйте переменные:
- `REDIS_HOST`
- `REDIS_PORT`

### 7. Деплой
1. Нажмите **Create Web Service**
2. Render автоматически соберет Docker образ
3. Дождитесь успешного деплоя (зеленая галочка)

### 8. Проверка
```bash
# Проверьте health endpoint
curl https://your-app-name.onrender.com/health

# Должен вернуть: {"ok": true}
```

## 🐳 Docker Hub + VPS

### 1. Сборка и публикация образа
```bash
# Сборка
docker build -t your-username/ai-tutor-server:latest .

# Публикация
docker push your-username/ai-tutor-server:latest
```

### 2. Настройка VPS
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Создание docker-compose.prod.yml
```yaml
version: "3.9"
services:
  api:
    image: your-username/ai-tutor-server:latest
    container_name: ai_tutor_api_prod
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_BASE_URL=${OPENAI_BASE_URL}
      - OPENAI_MODEL=${OPENAI_MODEL}
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
      - JWT_SECRET=${JWT_SECRET}
      - JWT_ALG=HS256
      - APP_CORS_ORIGINS=${APP_CORS_ORIGINS}
    ports:
      - "80:8000"
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    container_name: ai_tutor_pg_prod
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: ai_tutor_redis_prod
    restart: unless-stopped

volumes:
  pgdata:
```

### 4. Создание .env файла на VPS
```bash
# Создайте .env файл
nano .env

# Добавьте переменные
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
DB_USER=aitutor
DB_PASSWORD=strong_password_here
DB_NAME=aitutor
JWT_SECRET=your-super-secret-jwt-key
APP_CORS_ORIGINS=*
```

### 5. Запуск на VPS
```bash
# Запуск
docker compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker compose -f docker-compose.prod.yml ps

# Логи
docker compose -f docker-compose.prod.yml logs -f api
```

## ☁️ Google Cloud Run

### 1. Установка gcloud CLI
```bash
# Скачайте и установите с официального сайта
# https://cloud.google.com/sdk/docs/install
```

### 2. Аутентификация
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Включение API
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 4. Создание Dockerfile для Cloud Run
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 5. Деплой
```bash
# Сборка и деплой
gcloud run deploy ai-tutor-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="OPENAI_API_KEY=your_key,OPENAI_BASE_URL=https://api.openrouter.ai/v1"
```

## 🔒 Настройка безопасности

### 1. JWT Secret
```bash
# Генерация сильного секрета
openssl rand -hex 32
# Используйте результат как JWT_SECRET
```

### 2. CORS настройки
```python
# В app/config.py для продакшена
APP_CORS_ORIGINS = "https://yourdomain.com,https://app.yourdomain.com"
```

### 3. Rate Limiting (опционально)
```python
# Добавьте в requirements.txt
slowapi==0.1.9

# В main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/lesson/turn")
@limiter.limit("10/minute")
async def turn(request: Request, body: TurnRequest, db: AsyncSession = Depends(get_db)):
    # ... ваш код
```

## 📊 Мониторинг

### 1. Health Checks
```bash
# Автоматическая проверка
curl -f https://your-app.com/health || echo "Service down"
```

### 2. Логи
```bash
# Docker
docker logs -f container_name

# Render
# Логи доступны в веб-интерфейсе

# Cloud Run
gcloud logging read "resource.type=cloud_run_revision"
```

### 3. Метрики
```python
# Добавьте в requirements.txt
prometheus-client==0.17.1

# В main.py
from prometheus_client import Counter, Histogram, generate_latest

# Метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🚨 Troubleshooting

### Проблема: База данных не подключается
```bash
# Проверьте переменные окружения
echo $DB_HOST
echo $DB_PASSWORD

# Проверьте логи
docker logs postgres_container
```

### Проблема: Redis не подключается
```bash
# Проверьте доступность
docker exec -it redis_container redis-cli ping
# Должен ответить: PONG
```

### Проблема: LLM не отвечает
```bash
# Проверьте API ключ
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.openrouter.ai/v1/models

# Проверьте лимиты API
```

## 📱 Обновление Flutter приложения

После деплоя обновите `baseUrl` в Flutter:

```dart
class ApiConfig {
  // Продакшен
  static const String baseUrl = 'https://your-app.onrender.com';
  
  // Или ваш VPS
  // static const String baseUrl = 'http://your-vps-ip';
}
```

## 🎯 Следующие шаги

1. **SSL сертификат** - настройте HTTPS
2. **Backup базы** - автоматическое резервное копирование
3. **CDN** - для статических файлов
4. **Load Balancer** - для высокой нагрузки
5. **CI/CD** - автоматический деплой при push 