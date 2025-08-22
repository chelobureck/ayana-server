# Примеры использования Google OAuth API

## Настройка

### 1. Получение Google OAuth credentials

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google+ API
4. Создайте OAuth 2.0 credentials
5. Добавьте разрешенные redirect URIs для вашего приложения

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
GOOGLE_CLIENT_ID=your_google_client_id_here
JWT_SECRET=your_secure_jwt_secret_here
```

## API Endpoints

### 1. Регистрация/Вход через Google

**POST** `/auth/google`

**Request Body:**
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

### 2. Получение профиля пользователя

**GET** `/auth/profile`

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

### 3. Обновление токена

**POST** `/auth/refresh`

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

## Примеры использования

### JavaScript (Frontend)

```javascript
// Получение Google ID token
async function signInWithGoogle() {
  try {
    // Инициализация Google Sign-In
    const auth2 = await gapi.auth2.init({
      client_id: 'YOUR_GOOGLE_CLIENT_ID'
    });
    
    // Вход пользователя
    const googleUser = await auth2.signIn();
    const idToken = googleUser.getAuthResponse().id_token;
    
    // Отправка токена на сервер
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
    
    if (response.ok) {
      // Сохранение токена
      localStorage.setItem('access_token', data.access_token);
      
      if (data.is_new_user) {
        console.log('Новый пользователь зарегистрирован!');
      } else {
        console.log('Пользователь вошел в систему!');
      }
      
      // Получение профиля
      await getUserProfile(data.access_token);
    }
  } catch (error) {
    console.error('Ошибка входа:', error);
  }
}

// Получение профиля пользователя
async function getUserProfile(token) {
  try {
    const response = await fetch('/auth/profile', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const profile = await response.json();
      console.log('Профиль пользователя:', profile);
    }
  } catch (error) {
    console.error('Ошибка получения профиля:', error);
  }
}

// Обновление токена
async function refreshToken(token) {
  try {
    const response = await fetch('/auth/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      console.log('Токен обновлен!');
    }
  } catch (error) {
    console.error('Ошибка обновления токена:', error);
  }
}
```

### Python (Backend/Testing)

```python
import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_google_auth():
    """Тестирование Google OAuth API"""
    
    # Замените на реальный Google ID token
    google_id_token = "your_google_id_token_here"
    
    # Регистрация/вход через Google
    auth_response = requests.post(
        f"{BASE_URL}/auth/google",
        json={"id_token": google_id_token}
    )
    
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        print("Успешная аутентификация:", auth_data)
        
        # Получение профиля
        profile_response = requests.get(
            f"{BASE_URL}/auth/profile",
            headers={"Authorization": f"Bearer {auth_data['access_token']}"}
        )
        
        if profile_response.status_code == 200:
            profile = profile_response.json()
            print("Профиль пользователя:", profile)
        
        # Обновление токена
        refresh_response = requests.post(
            f"{BASE_URL}/auth/refresh",
            headers={"Authorization": f"Bearer {auth_data['access_token']}"}
        )
        
        if refresh_response.status_code == 200:
            refresh_data = refresh_response.json()
            print("Токен обновлен:", refresh_data)
    
    else:
        print("Ошибка аутентификации:", auth_response.text)

if __name__ == "__main__":
    test_google_auth()
```

### cURL

```bash
# Регистрация/вход через Google
curl -X POST "http://localhost:8000/auth/google" \
  -H "Content-Type: application/json" \
  -d '{"id_token": "your_google_id_token_here"}'

# Получение профиля (замените TOKEN на полученный access_token)
curl -X GET "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer TOKEN"

# Обновление токена
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Authorization: Bearer TOKEN"
```

## Безопасность

1. **JWT Secret**: Используйте длинный, случайный секрет для JWT
2. **HTTPS**: Всегда используйте HTTPS в продакшене
3. **Token Expiration**: Токены истекают через 24 часа
4. **Google Client ID**: Проверяйте Google Client ID на сервере
5. **Input Validation**: Все входные данные валидируются через Pydantic

## Обработка ошибок

API возвращает стандартные HTTP статус коды:

- `200` - Успешный запрос
- `400` - Неверный запрос
- `401` - Неавторизованный доступ
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

Все ошибки содержат детальное описание проблемы в поле `detail`.
