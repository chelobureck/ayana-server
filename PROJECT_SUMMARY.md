# 📋 AI Tutor Server - Краткое резюме

## 🎯 Что это?

**AI Tutor Server** - это готовый к запуску бэкенд для Flutter MVP с AI-репетитором. Сервер использует **FastAPI + PostgreSQL + Redis + Docker** и интегрируется с LLM через OpenAI-совместимый API.

## 🧠 Ключевые особенности

### AI Оркестрация
- **Две роли**: Айя (учитель) + Аяна (одноклассница)
- **Техника Фейнмана**: объяснение → вопросы → исправления → мини-проект
- **Промпты на русском** для дошкольников
- **Анимации**: LLM описывает что показать на экране

### Технический стек
- **FastAPI** - современный Python веб-фреймворк
- **PostgreSQL** - основная база данных (SQLAlchemy + Alembic-ready)
- **Redis** - кеш для LLM ответов (dedupe + TTL)
- **Docker** - контейнеризация для простого деплоя
- **OpenAI-compatible** - работает с любым LLM API

### API Endpoints
- `POST /lesson/turn` - **главный endpoint** для диалога
- `POST /auth/ensure-user` - управление пользователями
- `POST /project/create` - создание мини-проектов
- `GET /health` - проверка здоровья сервиса

## 🚀 Быстрый старт

```bash
# 1. Клонирование
git clone <repo>
cd ai-tutor-server

# 2. Настройка
cp env.example .env
# Заполните OPENAI_API_KEY в .env

# 3. Запуск
docker compose up --build

# 4. Проверка
curl http://localhost:8000/health
```

## 📱 Интеграция с Flutter

```dart
// Настройка baseUrl
static const String baseUrl = 'http://localhost:8000';

// Основной вызов
final response = await http.post(
  Uri.parse('$baseUrl/lesson/turn'),
  headers: {'Content-Type': 'application/json'},
  body: json.encode({
    'user_uid': 'demo123',
    'messages': [{'role': 'user', 'content': 'Почему 2+2=4?'}]
  }),
);
```

## 🎭 Пример диалога

```
Ребенок: "Почему 2+2=4?"
Айя: "Представь, что у тебя есть 2 яблока, и мама дала еще 2. Сколько всего?"
Ребенок: "4 яблока!"
Аяна: "А если у тебя 3 конфеты и папа дал еще 1?"
```

## 🔧 Архитектура

```
app/
├── main.py          # FastAPI приложение
├── config.py        # настройки (.env)
├── models.py        # SQLAlchemy модели
├── ai.py            # LLM интеграция
├── prompts.py       # промпты для ролей
├── cache.py         # Redis кеш
└── routers/         # API endpoints
    ├── health.py    # /health
    ├── auth.py      # /auth/*
    ├── lesson.py    # /lesson/* (основной)
    └── project.py   # /project/*
```

## 🌐 Деплой

### Render (рекомендуется)
- Автоматический деплой из Git
- Managed PostgreSQL + Redis
- Бесплатный план для MVP

### VPS + Docker
- Полный контроль
- Docker Compose
- Настройка SSL

### Google Cloud Run
- Serverless
- Автоматическое масштабирование
- Pay-per-use

## 💡 Преимущества

✅ **Готов к запуску** - все файлы созданы  
✅ **Docker-ready** - работает из коробки  
✅ **LLM-агностик** - любой OpenAI-совместимый API  
✅ **Flutter-ready** - готовые примеры интеграции  
✅ **Продакшен-ready** - инструкции по деплою  
✅ **Документирован** - подробные гайды  

## 🎯 Идеально для

- **Flutter MVP** с AI-репетитором
- **Образовательные приложения** для детей
- **Быстрый прототип** AI-сервиса
- **Изучение FastAPI** + современного Python
- **Деплой на облако** с минимальными настройками

## 📚 Документация

- **`START_HERE.md`** - начните отсюда
- **`QUICKSTART.md`** - быстрый старт за 5 минут
- **`deploy_guide.md`** - деплой на продакшен
- **`flutter_integration.md`** - интеграция с Flutter
- **`curl_examples.md`** - примеры API вызовов

---

**🚀 Проект готов к запуску! Просто следуйте `START_HERE.md`** 