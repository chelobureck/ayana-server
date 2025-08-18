# 🎯 AI Tutor Server - Начните здесь!

## 🚀 Быстрый запуск (5 минут)

### 1️⃣ Подготовка
```bash
# Убедитесь что у вас установлен Docker Desktop
docker --version

# Скопируйте конфигурацию
cp env.example .env
```

### 2️⃣ Настройка API ключа
Откройте `.env` и заполните **ОБЯЗАТЕЛЬНО**:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

**Где взять API ключ:**
- [OpenRouter](https://openrouter.ai/) - для Llama 4 Scout
- [Together AI](https://together.ai/) - альтернатива
- [Ollama](https://ollama.ai/) - локально

### 3️⃣ Запуск
```bash
# Windows
start.bat

# Mac/Linux
chmod +x start.sh
./start.sh

# Или вручную
docker compose up --build
```

### 4️⃣ Проверка
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

## 📚 Документация

- **`QUICKSTART.md`** - быстрый старт
- **`README.md`** - полное описание
- **`deploy_guide.md`** - деплой на продакшен
- **`flutter_integration.md`** - интеграция с Flutter
- **`curl_examples.md`** - примеры API вызовов

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
- В **разработке** можно передавать UID как токен

## 🆘 Нужна помощь?

1. Проверьте логи: `docker compose logs -f`
2. Убедитесь что все сервисы запущены: `docker compose ps`
3. Проверьте переменные окружения: `docker compose exec api env`
4. Создайте issue в репозитории

---

**🎉 Поздравляем! Ваш AI Tutor Server готов к работе!** 