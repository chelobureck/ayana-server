# 🚀 Быстрый старт AI Tutor Server

## ⚡ За 5 минут

### 1. Клонирование и настройка
```bash
git clone <your-repo>
cd ai-tutor-server
cp env.example .env
```

### 2. Настройка .env
Откройте `.env` и заполните:
```bash
# Обязательно!
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# Остальное можно оставить по умолчанию
```

### 3. Запуск
```bash
# Windows
start.bat

# Mac/Linux
chmod +x start.sh
./start.sh

# Или вручную
docker compose up --build
```

### 4. Проверка
```bash
curl http://localhost:8000/health
# Должен вернуть: {"ok": true}
```

## 🧪 Тестирование API

### Автоматическое тестирование
```bash
python test_api.py
```

### Ручное тестирование
```bash
# Создание пользователя
curl -X POST "http://localhost:8000/auth/ensure-user?uid=demo123&display_name=Kid"

# Диалог
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid":"demo123",
    "messages":[{"role":"user","content":"Почему 2+2=4?"}]
  }'
```

## 🔧 Разработка

### Локальный запуск без Docker
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Структура проекта
```
app/
├── main.py          # FastAPI приложение
├── config.py        # настройки
├── models.py        # SQLAlchemy модели
├── ai.py            # LLM интеграция
├── prompts.py       # промпты для ролей
└── routers/         # API endpoints
    ├── health.py    # /health
    ├── auth.py      # /auth/*
    ├── lesson.py    # /lesson/*
    └── project.py   # /project/*
```

## 📱 Интеграция с Flutter

### Настройка baseUrl
```dart
class ApiConfig {
  // Локально
  static const String baseUrl = 'http://localhost:8000';
  
  // На устройстве (замените IP)
  // static const String baseUrl = 'http://192.168.1.100:8000';
}
```

### Основные endpoints
- `POST /auth/ensure-user` - создание пользователя
- `POST /lesson/turn` - диалог с AI (основной)
- `POST /project/create` - создание проекта

## 🚨 Частые проблемы

### Docker не запускается
```bash
# Проверьте что Docker Desktop запущен
docker --version

# Очистите контейнеры
docker compose down -v
docker compose up --build
```

### База данных не подключается
```bash
# Проверьте .env файл
cat .env | grep DB_

# Перезапустите сервисы
docker compose restart postgres
```

### LLM не отвечает
```bash
# Проверьте API ключ
echo $OPENAI_API_KEY

# Проверьте доступность API
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.openrouter.ai/v1/models
```

## 📚 Документация

- `README.md` - полное описание
- `deploy_guide.md` - деплой на продакшен
- `flutter_integration.md` - интеграция с Flutter
- `curl_examples.md` - примеры API вызовов

## 🎯 Следующие шаги

1. **Настройте API ключ** в `.env`
2. **Запустите сервер** через Docker
3. **Протестируйте API** через `test_api.py`
4. **Интегрируйте с Flutter** используя примеры
5. **Деплой на продакшен** по `deploy_guide.md`

## 💡 Советы

- Используйте **OpenRouter** для доступа к Llama 4 Scout
- В **разработке** можно передавать UID как токен
- **CORS** настроен для всех источников в dev режиме
- **Redis** кеширует LLM ответы для экономии API вызовов 