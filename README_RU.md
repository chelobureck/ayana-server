# 🎯 AI Tutor Server (FastAPI + Postgres + Redis + Docker)

**Готовый к запуску бэкенд для Flutter MVP с AI-репетитором** 🚀

## 📋 Что это?

AI Tutor Server - это полнофункциональный бэкенд для образовательного приложения с двумя AI-ролями:
- **Айя** - добрый учитель, объясняет просто и понятно
- **Аяна** - одноклассница, задает вопросы и ведет к мини-проектам

Использует **технику Фейнмана**: объяснение → вопросы → исправления → практика.

## 🚀 Быстрый старт (5 минут)

### 1. Подготовка
```bash
# Убедитесь что Docker Desktop запущен
docker --version

# Скопируйте конфигурацию
cp env.example .env
```

### 2. Настройка API ключа
Откройте `.env` и заполните **ОБЯЗАТЕЛЬНО**:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
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

## 🧪 Тестирование

### Автоматическое тестирование
```bash
python test_api.py
```

### Ручное тестирование
```bash
# Создание пользователя
curl -X POST "http://localhost:8000/auth/ensure-user?uid=demo123&display_name=Kid"

# Диалог с AI
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid":"demo123",
    "messages":[{"role":"user","content":"Почему 2+2=4?"}]
  }'
```

## 📱 Интеграция с Flutter

### Настройка baseUrl
```dart
class ApiConfig {
  // Локально
  static const String baseUrl = 'http://localhost:8000';
  
  // На устройстве (замените на ваш IP)
  // static const String baseUrl = 'http://192.168.1.100:8000';
}
```

### Основные endpoints
- `POST /lesson/turn` - **главный endpoint** для диалога с AI
- `POST /auth/ensure-user` - создание пользователя
- `POST /project/create` - создание проекта

## 🎭 Как это работает

### Роли AI
1. **Айя** - учитель, объясняет просто и понятно
2. **Аяна** - одноклассница, задает вопросы и ведет к проекту

### Техника Фейнмана
- Простое объяснение → Вопросы → Исправления → Мини-проект

### Пример диалога
```
Ребенок: "Почему 2+2=4?"
Айя: "Представь, что у тебя есть 2 яблока, и мама дала еще 2. Сколько всего?"
Ребенок: "4 яблока!"
Аяна: "А если у тебя 3 конфеты и папа дал еще 1?"
```

## 🔧 Технический стек

- **FastAPI** - современный Python веб-фреймворк
- **PostgreSQL** - основная база данных (SQLAlchemy + Alembic-ready)
- **Redis** - кеш для LLM ответов (dedupe + TTL)
- **Docker** - контейнеризация для простого деплоя
- **OpenAI-compatible** - работает с любым LLM API

## 📁 Структура проекта

```
ai-tutor-server/
├── WELCOME.md              # 🎉 Добро пожаловать!
├── START_HERE.md           # 🎯 Начните отсюда!
├── QUICKSTART.md           # ⚡ Быстрый старт за 5 минут
├── FIRST_RUN.md            # 🚀 Первый запуск для новичков
├── GETTING_STARTED.md      # 📚 Полное руководство
├── CHECKLIST.md            # ✅ Чек-лист готовности
├── PROJECT_SUMMARY.md      # 📋 Краткое резюме
├── FILES_OVERVIEW.md       # 📁 Обзор всех файлов
├── USAGE_GUIDE.md          # 📖 Руководство по использованию
├── deploy_guide.md         # 🚀 Деплой на продакшен
├── flutter_integration.md  # 📱 Интеграция с Flutter
├── curl_examples.md        # 🧪 Примеры API вызовов
├── app/                    # 🐍 Python приложение
│   ├── main.py            # FastAPI приложение
│   ├── config.py          # настройки
│   ├── models.py          # SQLAlchemy модели
│   ├── ai.py              # LLM интеграция
│   ├── prompts.py         # промпты для ролей
│   ├── cache.py           # Redis кеш
│   └── routers/           # API endpoints
├── requirements.txt        # Python зависимости
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Локальная разработка
├── render.yaml            # Деплой на Render
├── start.bat              # Запуск для Windows
├── start.ps1              # Запуск для PowerShell
├── start.sh               # Запуск для Linux/Mac
└── test_api.py            # Python тесты
```

## 🌐 Деплой

### Render (рекомендуется для MVP)
- Автоматический деплой из Git
- Managed PostgreSQL + Redis
- Бесплатный план для MVP
- Подробные инструкции в `deploy_guide.md`

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

### 🎯 **Основные файлы для начала:**
- **`WELCOME.md`** - 🎉 добро пожаловать!
- **`START_HERE.md`** - 🎯 **начните отсюда!**
- **`QUICKSTART.md`** - ⚡ быстрый старт за 5 минут
- **`FIRST_RUN.md`** - 🚀 первый запуск для новичков
- **`GETTING_STARTED.md`** - 📚 полное руководство

### 📋 **Информационные файлы:**
- **`CHECKLIST.md`** - ✅ чек-лист готовности
- **`PROJECT_SUMMARY.md`** - 📋 краткое резюме
- **`FILES_OVERVIEW.md`** - 📁 обзор всех файлов

### 🔧 **Технические файлы:**
- **`USAGE_GUIDE.md`** - 📖 руководство по использованию
- **`deploy_guide.md`** - 🚀 деплой на продакшен
- **`flutter_integration.md`** - 📱 интеграция с Flutter
- **`curl_examples.md`** - 🧪 примеры API вызовов

## 🚨 Решение проблем

### Docker не запускается
```bash
# Проверьте Docker Desktop
docker --version

# Очистите и перезапустите
docker compose down -v
docker compose up --build
```

### API не отвечает
```bash
# Проверьте .env файл
cat .env | grep OPENAI

# Проверьте логи
docker compose logs api
```

### База данных не подключается
```bash
# Перезапустите PostgreSQL
docker compose restart postgres
```

## 🆘 Нужна помощь?

1. Проверьте логи: `docker compose logs -f`
2. Убедитесь что все сервисы запущены: `docker compose ps`
3. Проверьте переменные окружения: `docker compose exec api env`
4. Создайте issue в репозитории

## 🎯 Следующие шаги

1. ✅ **Запустите сервер** (вы уже здесь!)
2. 🔑 **Настройте API ключ** в `.env`
3. 🧪 **Протестируйте API** через `test_api.py`
4. 📱 **Интегрируйте с Flutter** используя примеры
5. 🚀 **Деплой на продакшен** по `deploy_guide.md`

## 💡 Полезные советы

- **OpenRouter** - лучший выбор для Llama 4 Scout
- **Redis** кеширует ответы LLM для экономии API вызовов
- **CORS** настроен для всех источников в dev режиме
- В **разработке** можно передавать UID напрямую как токен

---

## 🎉 Поздравляем!

**Ваш AI Tutor Server полностью готов к работе!**

Просто следуйте `START_HERE.md` и начните разработку Flutter приложения с AI-репетитором.

---

**💡 Главный совет**: Начните с `START_HERE.md` - это ваш основной файл для начала работы!

**🚀 Удачи с вашим проектом!** 