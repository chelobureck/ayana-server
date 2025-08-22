# Настройка Google OAuth для Ayana AI

## 🚀 Быстрый старт

### 1. Создание проекта в Google Cloud Console

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google+ API:
   - Перейдите в "APIs & Services" > "Library"
   - Найдите "Google+ API" и включите его
   - Также включите "Google Identity and Access Management (IAM) API"

### 2. Создание OAuth 2.0 credentials

1. В "APIs & Services" > "Credentials" нажмите "Create Credentials"
2. Выберите "OAuth 2.0 Client IDs"
3. Настройте OAuth consent screen:
   - User Type: External (для публичного доступа)
   - App name: "Ayana AI"
   - User support email: ваш email
   - Developer contact information: ваш email
   - Scopes: добавьте `email`, `profile`, `openid`

4. Создайте OAuth 2.0 Client ID:
   - Application type: Web application
   - Name: "Ayana AI Web Client"
   - Authorized JavaScript origins: добавьте домены вашего приложения
     - `http://localhost:3000` (для разработки)
     - `http://localhost:8000` (для разработки)
     - Ваш продакшн домен
   - Authorized redirect URIs: добавьте
     - `http://localhost:3000/auth/callback`
     - `http://localhost:8000/auth/callback`
     - Ваш продакшн callback URL

### 3. Получение Client ID

После создания credentials вы получите:
- **Client ID** - скопируйте его
- **Client Secret** - не нужен для ID token verification

## 🔧 Настройка приложения

### 1. Обновление переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here

# JWT Security
JWT_SECRET=your_very_long_random_secret_key_here
JWT_ALG=HS256

# Остальные настройки...
APP_HOST=0.0.0.0
APP_PORT=8000
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=aitutor
```

### 2. Генерация JWT Secret

Для продакшена используйте длинный случайный секрет:

```bash
# Linux/Mac
openssl rand -hex 64

# Windows PowerShell
$bytes = New-Object Byte[] 64
(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
[Convert]::ToHexString($bytes)
```

## 📱 Интеграция на фронтенде

### 1. Установка Google Sign-In

Добавьте Google Sign-In в ваш HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Ayana AI - Вход через Google</title>
    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <meta name="google-signin-client_id" content="YOUR_GOOGLE_CLIENT_ID">
</head>
<body>
    <div id="google-signin-button"></div>
    
    <script>
        function onSignIn(googleUser) {
            const idToken = googleUser.getAuthResponse().id_token;
            signInWithGoogle(idToken);
        }
        
        function signInWithGoogle(idToken) {
            fetch('/auth/google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id_token: idToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.access_token) {
                    localStorage.setItem('access_token', data.access_token);
                    if (data.is_new_user) {
                        alert('Добро пожаловать! Вы успешно зарегистрированы.');
                    } else {
                        alert('Добро пожаловать обратно!');
                    }
                    // Перенаправление на главную страницу
                    window.location.href = '/dashboard';
                }
            })
            .catch(error => {
                console.error('Ошибка входа:', error);
                alert('Ошибка входа. Попробуйте еще раз.');
            });
        }
        
        function signOut() {
            const auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut().then(function () {
                localStorage.removeItem('access_token');
                window.location.href = '/login';
            });
        }
    </script>
    
    <div class="g-signin2" data-onsuccess="onSignIn"></div>
    <button onclick="signOut()">Выйти</button>
</body>
</html>
```

### 2. React компонент (если используете React)

```jsx
import React, { useEffect, useState } from 'react';

const GoogleSignIn = () => {
    const [isSignedIn, setIsSignedIn] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Инициализация Google Sign-In
        window.gapi.load('auth2', () => {
            window.gapi.auth2.init({
                client_id: 'YOUR_GOOGLE_CLIENT_ID'
            }).then((auth2) => {
                if (auth2.isSignedIn.get()) {
                    handleSignIn(auth2.currentUser.get());
                }
            });
        });
    }, []);

    const handleSignIn = async (googleUser) => {
        try {
            const idToken = googleUser.getAuthResponse().id_token;
            
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
                setIsSignedIn(true);
                setUser(data);
                
                if (data.is_new_user) {
                    alert('Добро пожаловать! Вы успешно зарегистрированы.');
                }
            }
        } catch (error) {
            console.error('Ошибка входа:', error);
        }
    };

    const signOut = () => {
        const auth2 = window.gapi.auth2.getAuthInstance();
        auth2.signOut().then(() => {
            localStorage.removeItem('access_token');
            setIsSignedIn(false);
            setUser(null);
        });
    };

    return (
        <div>
            {!isSignedIn ? (
                <div className="g-signin2" data-onsuccess="handleSignIn"></div>
            ) : (
                <div>
                    <p>Добро пожаловать, {user?.display_name}!</p>
                    <button onClick={signOut}>Выйти</button>
                </div>
            )}
        </div>
    );
};

export default GoogleSignIn;
```

## 🧪 Тестирование

### 1. Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python -m uvicorn app.main:app --reload

# В другом терминале запуск тестов
python test_google_oauth.py
```

### 2. Ручное тестирование

```bash
# Тестирование с cURL
curl -X POST "http://localhost:8000/auth/google" \
  -H "Content-Type: application/json" \
  -d '{"id_token": "your_google_id_token_here"}'
```

## 🔒 Безопасность

### 1. Проверки на сервере

- ✅ Верификация Google ID token
- ✅ Проверка издателя токена (accounts.google.com)
- ✅ Проверка срока действия токена
- ✅ Валидация входных данных через Pydantic
- ✅ JWT токены с ограниченным временем жизни

### 2. Рекомендации

- Используйте HTTPS в продакшене
- Регулярно обновляйте JWT_SECRET
- Ограничьте CORS origins только необходимыми доменами
- Мониторьте попытки неавторизованного доступа
- Логируйте все аутентификации

## 🚨 Устранение неполадок

### 1. Ошибка "GOOGLE_CLIENT_ID is not configured"

**Решение:** Проверьте, что в `.env` файле установлен `GOOGLE_CLIENT_ID`

### 2. Ошибка "Invalid Google ID token"

**Возможные причины:**
- Неверный Client ID
- Токен истек
- Токен от другого приложения
- Проблемы с Google API

**Решение:**
- Проверьте правильность Client ID
- Убедитесь, что токен получен от правильного приложения
- Проверьте статус Google API

### 3. Ошибка "Wrong issuer"

**Решение:** Проверьте, что используете правильный Google Client ID

### 4. Проблемы с CORS

**Решение:** Настройте CORS в FastAPI приложении:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 Дополнительные ресурсы

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Sign-In Documentation](https://developers.google.com/identity/sign-in/web)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - для отладки JWT токенов

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи сервера
2. Убедитесь, что все переменные окружения установлены
3. Проверьте, что Google API включены
4. Убедитесь, что Client ID правильный
5. Проверьте настройки CORS

Для получения дополнительной помощи создайте issue в репозитории проекта.
