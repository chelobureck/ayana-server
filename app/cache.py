import redis
from .config import settings
import json
from typing import Optional, Any
from datetime import timedelta

# Подключение к Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

class TokenCache:
    """Класс для работы с временными токенами в кэше"""
    
    @staticmethod
    def store_verification_token(email: str, token: str, expires_in: int = 45) -> bool:
        """
        Сохраняет токен подтверждения в кэш
        
        Args:
            email: Email пользователя
            token: Токен подтверждения
            expires_in: Время жизни токена в секундах
            
        Returns:
            True если токен сохранен успешно
        """
        try:
            key = f"verification_token:{email}"
            data = {
                "token": token,
                "email": email,
                "created_at": str(timedelta(seconds=0))
            }
            
            # Сохраняем токен с временем жизни
            redis_client.setex(
                key,
                expires_in,
                json.dumps(data)
            )
            
            return True
        except Exception as e:
            print(f"Error storing verification token: {e}")
            return False
    
    @staticmethod
    def get_verification_token(email: str) -> Optional[str]:
        """
        Получает токен подтверждения из кэша
        
        Args:
            email: Email пользователя
            
        Returns:
            Токен если найден, None иначе
        """
        try:
            key = f"verification_token:{email}"
            data = redis_client.get(key)
            
            if data:
                token_data = json.loads(data)
                return token_data.get("token")
            
            return None
        except Exception as e:
            print(f"Error getting verification token: {e}")
            return None
    
    @staticmethod
    def delete_verification_token(email: str) -> bool:
        """
        Удаляет токен подтверждения из кэша
        
        Args:
            email: Email пользователя
            
        Returns:
            True если токен удален успешно
        """
        try:
            key = f"verification_token:{email}"
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Error deleting verification token: {e}")
            return False
    
    @staticmethod
    def store_password_reset_token(email: str, token: str, expires_in: int = 45) -> bool:
        """
        Сохраняет токен для сброса пароля в кэш
        
        Args:
            email: Email пользователя
            token: Токен для сброса пароля
            expires_in: Время жизни токена в секундах
            
        Returns:
            True если токен сохранен успешно
        """
        try:
            key = f"password_reset_token:{email}"
            data = {
                "token": token,
                "email": email,
                "created_at": str(timedelta(seconds=0))
            }
            
            redis_client.setex(
                key,
                expires_in,
                json.dumps(data)
            )
            
            return True
        except Exception as e:
            print(f"Error storing password reset token: {e}")
            return False
    
    @staticmethod
    def get_password_reset_token(email: str) -> Optional[str]:
        """
        Получает токен для сброса пароля из кэша
        
        Args:
            email: Email пользователя
            
        Returns:
            Токен если найден, None иначе
        """
        try:
            key = f"password_reset_token:{email}"
            data = redis_client.get(key)
            
            if data:
                token_data = json.loads(data)
                return token_data.get("token")
            
            return None
        except Exception as e:
            print(f"Error getting password reset token: {e}")
            return None
    
    @staticmethod
    def delete_password_reset_token(email: str) -> bool:
        """
        Удаляет токен для сброса пароля из кэша
        
        Args:
            email: Email пользователя
            
        Returns:
            True если токен удален успешно
        """
        try:
            key = f"password_reset_token:{email}"
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Error deleting password reset token: {e}")
            return False


def set_cached_completion(key: str, value: Any, expires_in: int = 300) -> bool:
    """
    Сохраняет результат в кэш
    """
    try:
        redis_client.setex(f"completion:{key}", expires_in, json.dumps(value))
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False


def get_cached_completion(key: str) -> Optional[Any]:
    """
    Получает результат из кэша
    """
    try:
        data = redis_client.get(f"completion:{key}")
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None

# Создаем глобальный экземпляр кэша токенов
token_cache = TokenCache() 