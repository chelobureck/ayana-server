# Google OAuth API для Ayana AI

## 🎯 Обзор

Этот модуль добавляет полноценную поддержку аутентификации и регистрации пользователей через Google OAuth 2.0 в ваше приложение Ayana AI.

## ✨ Возможности

- 🔐 **Аутентификация через Google** - безопасный вход с использованием Google аккаунта
- 📝 **Автоматическая регистрация** - новые пользователи создаются автоматически
- 🔄 **JWT токены** - безопасные токены доступа с ограниченным временем жизни
- 👤 **Профили пользователей** - получение и управление информацией о пользователе
- 🔁 **Обновление токенов** - автоматическое обновление истекших токенов
- 🛡️ **Безопасность** - верификация Google ID токенов на сервере

## 🚀 Быстрый старт

### 1. Установка зависимостей

Все необходимые зависимости уже включены в `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Настройка Google OAuth

1. **Создайте проект в Google Cloud Console:**
   - Перейдите на [console.cloud.google.com](https://console.cloud.google.com/)
   - Создайте новый проект или выберите существующий
   - Включите Google+ API

2. **Создайте OAuth 2.0 credentials:**
   - В "APIs & Services" > "Credentials" нажмите "Create Credentials"
   - Выберите "OAuth 2.0 Client IDs"
   - Application type: Web application
   - Добавьте разрешенные домены (localhost для разработки)

3. **Настройте переменные окружения:**
   ```bash
   # Создайте файл .env
   cp env.example .env
   
   # Отредактируйте .env файл
   GOOGLE_CLIENT_ID=your_google_client_id_here
   JWT_SECRET=your_very_long_random_secret_key_here
   ```

### 3. Запуск приложения

```bash
# Запуск сервера
python -m uvicorn app.main:app --reload

# Или используйте скрипт запуска
./start.sh  # Linux/Mac
# или
start.ps1   # Windows PowerShell
```

## 📡 API Endpoints

### POST `/auth/google`
**Регистрация/вход через Google**

**Request:**
```json
{
  "id_token": "google_id_token_from_client"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user_id": 123,
  "user_uid": "google:123456789",
  "display_name": "Иван Иванов",
  "email": "ivan@example.com",
  "is_new_user": true
}
```

### GET `/auth/profile`
**Получение профиля пользователя**

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "user_id": 123,
  "user_uid": "google:123456789",
  "display_name": "Иван Иванов",
  "email": "ivan@example.com",
  "created_at": "2024-01-15T10:30:00",
  "sessions_count": 5
}
```

### POST `/auth/refresh`
**Обновление JWT токена**

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "access_token": "new_jwt_token_here",
  "token_type": "bearer",
  "expires_in": 86400
}
```

## 🧪 Тестирование

### Автоматические тесты

```bash
# Запуск всех тестов Google OAuth
python test_google_oauth.py

# Установка переменной окружения для тестирования
export GOOGLE_ID_TOKEN="your_test_token_here"
python test_google_oauth.py
```

### Ручное тестирование

```bash
# Тестирование с cURL
curl -X POST "http://localhost:8000/auth/google" \
  -H "Content-Type: application/json" \
  -d '{"id_token": "your_google_id_token_here"}'

# Получение профиля
curl -X GET "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Демонстрационная страница

Откройте `google_oauth_demo.html` в браузере для интерактивного тестирования:

1. Замените `YOUR_GOOGLE_CLIENT_ID` на ваш реальный Client ID
2. Убедитесь, что сервер запущен на localhost:8000
3. Нажмите кнопку "Войти через Google"

## 🔧 Интеграция на фронтенде

### JavaScript (Vanilla)

```javascript
// Вход через Google
async function signInWithGoogle(idToken) {
    try {
        const response = await fetch('/auth/google', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_token: idToken
            })
        });
        
        const data = await response.json();
        
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            
            if (data.is_new_user) {
                console.log('Новый пользователь зарегистрирован!');
            }
            
            return data;
        }
    } catch (error) {
        console.error('Ошибка входа:', error);
        throw error;
    }
}

// Получение профиля
async function getUserProfile() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        throw new Error('Нет токена доступа');
    }
    
    const response = await fetch('/auth/profile', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return response.json();
}
```

### React Hook

```jsx
import { useState, useEffect } from 'react';

const useGoogleAuth = () => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(false);

    const signIn = async (idToken) => {
        setLoading(true);
        try {
            const response = await fetch('/auth/google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id_token: idToken })
            });
            
            const data = await response.json();
            
            if (data.access_token) {
                setToken(data.access_token);
                setUser(data);
                localStorage.setItem('access_token', data.access_token);
                return data;
            }
        } catch (error) {
            console.error('Ошибка входа:', error);
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const signOut = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('access_token');
    };

    const refreshToken = async () => {
        if (!token) return;
        
        try {
            const response = await fetch('/auth/refresh', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const data = await response.json();
            
            if (data.access_token) {
                setToken(data.access_token);
                localStorage.setItem('access_token', data.access_token);
            }
        } catch (error) {
            console.error('Ошибка обновления токена:', error);
            signOut();
        }
    };

    useEffect(() => {
        const savedToken = localStorage.getItem('access_token');
        if (savedToken) {
            setToken(savedToken);
            // Можно также загрузить профиль пользователя
        }
    }, []);

    return {
        user,
        token,
        loading,
        signIn,
        signOut,
        refreshToken
    };
};

export default useGoogleAuth;
```

## 🔒 Безопасность

### Проверки на сервере

- ✅ **Верификация Google ID token** - проверка подлинности токена
- ✅ **Проверка издателя** - только tokens от accounts.google.com
- ✅ **Проверка срока действия** - автоматическое отклонение истекших токенов
- ✅ **Валидация данных** - все входные данные проверяются через Pydantic
- ✅ **JWT безопасность** - токены с ограниченным временем жизни (24 часа)

### Рекомендации

- 🔐 Используйте HTTPS в продакшене
- 🔑 Регулярно обновляйте JWT_SECRET
- 🌐 Ограничьте CORS origins только необходимыми доменами
- 📊 Мониторьте попытки неавторизованного доступа
- 📝 Логируйте все аутентификации

## 🚨 Устранение неполадок

### Частые проблемы

1. **"GOOGLE_CLIENT_ID is not configured"**
   - Проверьте, что в `.env` файле установлен `GOOGLE_CLIENT_ID`

2. **"Invalid Google ID token"**
   - Проверьте правильность Client ID
   - Убедитесь, что токен получен от правильного приложения
   - Проверьте статус Google API

3. **"Wrong issuer"**
   - Проверьте, что используете правильный Google Client ID

4. **Проблемы с CORS**
   - Настройте CORS в FastAPI приложении
   - Убедитесь, что домены добавлены в разрешенные origins

### Логи и отладка

```python
# Включите подробное логирование
import logging
logging.basicConfig(level=logging.DEBUG)

# Проверьте переменные окружения
import os
print("GOOGLE_CLIENT_ID:", os.getenv("GOOGLE_CLIENT_ID"))
print("JWT_SECRET:", os.getenv("JWT_SECRET"))
```

## 📚 Дополнительные ресурсы

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Sign-In Documentation](https://developers.google.com/identity/sign-in/web)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - для отладки JWT токенов

## 🤝 Поддержка

Если у вас возникли проблемы:

1. 📖 Проверьте документацию выше
2. 🔍 Изучите логи сервера
3. ✅ Убедитесь, что все переменные окружения установлены
4. 🌐 Проверьте, что Google API включены
5. 🔑 Убедитесь, что Client ID правильный
6. 🌍 Проверьте настройки CORS

Для получения дополнительной помощи создайте issue в репозитории проекта.

## 📝 Лицензия

Этот модуль является частью проекта Ayana AI и распространяется под той же лицензией.
