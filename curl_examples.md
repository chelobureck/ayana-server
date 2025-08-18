# 🧪 Примеры cURL команд для тестирования API

## 🔍 Проверка здоровья сервиса
```bash
curl -X GET "http://localhost:8000/health"
```

## 👤 Создание/получение пользователя
```bash
curl -X POST "http://localhost:8000/auth/ensure-user?uid=demo123&display_name=Тестовый%20ребенок"
```

## 📚 Создание сессии урока
```bash
curl -X POST http://localhost:8000/lesson/create-session \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid": "demo123",
    "topic": "Математика для малышей"
  }'
```

## 💬 Диалог с AI (основной endpoint)
```bash
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid": "demo123",
    "session_id": 1,
    "messages": [
      {
        "role": "user",
        "content": "Почему 2+2=4?"
      }
    ]
  }'
```

## 🔄 Продолжение диалога
```bash
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid": "demo123",
    "session_id": 1,
    "messages": [
      {
        "role": "user",
        "content": "Почему 2+2=4?"
      },
      {
        "role": "ayya",
        "content": "Представь, что у тебя есть 2 яблока, и мама дала еще 2. Сколько всего яблок?"
      },
      {
        "role": "user",
        "content": "4 яблока!"
      }
    ]
  }'
```

## 🧪 Создание проекта
```bash
curl -X POST http://localhost:8000/project/create \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "title": "Мой первый математический проект"
  }'
```

## 🌐 Тестирование с внешним сервером
Если ваш сервер запущен на другом IP (например, для Flutter):
```bash
# Замените IP на ваш локальный IP
curl -X GET "http://192.168.1.100:8000/health"
```

## 🔐 Тестирование с аутентификацией (для продакшена)
```bash
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token_here" \
  -d '{
    "user_uid": "demo123",
    "session_id": 1,
    "messages": [
      {
        "role": "user",
        "content": "Расскажи про цвета"
      }
    ]
  }'
```

## 📊 Проверка ответов
Все ответы от `/lesson/turn` имеют формат:
```json
{
  "role": "ayya|ayana|system",
  "say": "Текст ответа",
  "animations": ["анимация 1", "анимация 2"],
  "next_task": "следующее задание (опционально)"
}
```

## 🚀 Автоматическое тестирование
Запустите Python скрипт для полного тестирования:
```bash
python test_api.py
``` 