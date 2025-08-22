# Система авторизации Ayana AI

## 🎯 Обзор

Новая система авторизации и регистрации для Ayana AI с поддержкой:
- Регистрации по нику, email и паролю
- Подтверждения email через 7-значные токены
- Временных токенов с ограниченным временем жизни (45 секунд)
- Безопасного хранения паролей с bcrypt
- Интеграции с Redis для кэширования токенов
- Отправки email через SMTP

## ✨ Основные возможности

### 🔐 Аутентификация
- **Регистрация** - создание аккаунта с ник, email и паролем
- **Вход** - аутентификация по нику и паролю
- **Подтверждение email** - верификация через временные токены
- **Сброс пароля** - восстановление доступа через email

### 🛡️ Безопасность
- **Хеширование паролей** - bcrypt с солью
- **Временные токены** - 7-значные коды, действительные 45 секунд
- **JWT токены** - безопасные токены доступа
- **Валидация данных** - проверка через Pydantic схемы

### 📧 Email функциональность
- **Подтверждение регистрации** - автоматическая отправка токенов
- **Сброс пароля** - токены для восстановления доступа
- **HTML шаблоны** - красивые письма с брендингом
- **SMTP интеграция** - поддержка Gmail и других провайдеров

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `env.example`:

```env
# Email settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_TLS=true

# Verification token settings
VERIFICATION_TOKEN_LENGTH=7
VERIFICATION_TOKEN_EXPIRE_SECONDS=45

# JWT Security
JWT_SECRET=your_very_long_random_secret_key_here
JWT_ALG=HS256
JWT_EXPIRE_HOURS=24

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=aitutor

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 3. Настройка Gmail для отправки email

1. Включите двухфакторную аутентификацию в Google аккаунте
2. Создайте пароль приложения:
   - Перейдите в настройки безопасности
   - Выберите "Пароли приложений"
   - Создайте новый пароль для "Почта"
3. Используйте этот пароль в `SMTP_PASSWORD`

### 4. Запуск приложения

```bash
# Запуск сервера
python -m uvicorn app.main:app --reload

# Или используйте скрипт запуска
./start.sh  # Linux/Mac
# или
start.ps1   # Windows PowerShell
```

## 📡 API Endpoints

### POST `/auth/register`
**Регистрация нового пользователя**

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "password_confirm": "secure123"
}
```

**Response:**
```json
{
  "message": "Пользователь зарегистрирован. Проверьте email для подтверждения.",
  "token_sent": true,
  "expires_in": 45
}
```

### POST `/auth/verify-email`
**Подтверждение email с помощью токена**

**Request:**
```json
{
  "email": "john@example.com",
  "token": "1234567"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user_id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "is_verified": true
}
```

### POST `/auth/login`
**Вход пользователя**

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user_id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "is_verified": true
}
```

### POST `/auth/resend-verification`
**Повторная отправка токена подтверждения**

**Request:**
```json
{
  "email": "john@example.com"
}
```

### POST `/auth/forgot-password`
**Запрос на сброс пароля**

**Request:**
```json
{
  "email": "john@example.com"
}
```

### POST `/auth/reset-password`
**Сброс пароля с помощью токена**

**Request:**
```json
{
  "email": "john@example.com",
  "token": "1234567",
  "new_password": "newsecure123",
  "new_password_confirm": "newsecure123"
}
```

### GET `/auth/profile`
**Получение профиля пользователя**

**Headers:**
```
Authorization: Bearer jwt_token_here
```

## 🔧 Архитектура системы

### Модули

1. **`app/schemas.py`** - Pydantic схемы для валидации данных
2. **`app/models.py`** - SQLAlchemy модели для базы данных
3. **`app/auth.py`** - Основная логика аутентификации
4. **`app/email_service.py`** - Сервис для отправки email
5. **`app/password_utils.py`** - Утилиты для работы с паролями
6. **`app/cache.py`** - Redis кэш для временных токенов

### База данных

#### Таблица `users`
- `id` - первичный ключ
- `username` - уникальный ник пользователя
- `email` - уникальный email
- `password_hash` - хеш пароля
- `is_verified` - статус подтверждения email
- `created_at` - дата создания

#### Таблица `verification_tokens`
- `id` - первичный ключ
- `email` - email пользователя
- `token` - 7-значный токен
- `expires_at` - время истечения
- `is_used` - использован ли токен
- `created_at` - дата создания

### Кэширование

Токены хранятся в Redis с автоматическим истечением:
- **Ключ**: `verification_token:{email}`
- **Время жизни**: 45 секунд
- **Данные**: JSON с токеном и метаданными

## 📱 Демонстрационная страница

Откройте `auth_demo.html` в браузере для тестирования:

1. **Регистрация** - создание нового аккаунта
2. **Подтверждение email** - ввод 7-значного токена
3. **Вход** - аутентификация по нику и паролю
4. **Сброс пароля** - восстановление доступа

## 🧪 Тестирование

### Автоматические тесты

```bash
# Запуск тестов (требует настройки email)
python -m pytest tests/test_auth.py
```

### Ручное тестирование

```bash
# Регистрация пользователя
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "test123",
    "password_confirm": "test123"
  }'

# Подтверждение email
curl -X POST "http://localhost:8000/auth/verify-email" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "token": "1234567"
  }'

# Вход в систему
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "test123"
  }'
```

## 🔒 Безопасность

### Пароли
- Минимальная длина: 6 символов
- Требования: буквы + цифры
- Хеширование: bcrypt с солью

### Токены
- Длина: 7 цифр
- Время жизни: 45 секунд
- Хранение: Redis с автоматическим истечением

### JWT токены
- Алгоритм: HS256
- Время жизни: 24 часа (настраивается)
- Секрет: настраивается через переменные окружения

## 🚨 Устранение неполадок

### Проблемы с email

1. **"SMTP authentication failed"**
   - Проверьте правильность `SMTP_USER` и `SMTP_PASSWORD`
   - Убедитесь, что включена двухфакторная аутентификация
   - Используйте пароль приложения, а не основной пароль

2. **"Connection refused"**
   - Проверьте настройки `SMTP_HOST` и `SMTP_PORT`
   - Убедитесь, что SMTP сервер доступен

### Проблемы с токенами

1. **"Токен не найден или истек"**
   - Токены действительны только 45 секунд
   - Используйте `/auth/resend-verification` для получения нового

2. **"Неверный токен подтверждения"**
   - Проверьте правильность введенного токена
   - Убедитесь, что токен не истек

### Проблемы с базой данных

1. **"User with username already exists"**
   - Ники должны быть уникальными
   - Выберите другой ник

2. **"User with email already exists"**
   - Email должен быть уникальным
   - Используйте другой email или восстановите пароль

## 📚 Дополнительные ресурсы

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [bcrypt Documentation](https://github.com/pyca/bcrypt/)
- [Redis Python Client](https://redis-py.readthedocs.io/)
- [SMTP Python](https://docs.python.org/3/library/smtplib.html)

## 🤝 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи сервера
2. Убедитесь, что все переменные окружения установлены
3. Проверьте подключение к Redis и базе данных
4. Убедитесь, что SMTP сервер доступен
5. Проверьте настройки Gmail (если используете)

Для получения дополнительной помощи создайте issue в репозитории проекта.
