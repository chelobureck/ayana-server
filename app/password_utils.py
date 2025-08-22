import bcrypt
from typing import Tuple

def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        Хешированный пароль
    """
    # Генерируем соль и хешируем пароль
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль против хеша
    
    Args:
        password: Пароль в открытом виде
        hashed_password: Хешированный пароль
        
    Returns:
        True если пароль верный, False иначе
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Проверяет сложность пароля
    
    Args:
        password: Пароль для проверки
        
    Returns:
        Tuple[bool, str]: (валиден ли пароль, сообщение об ошибке)
    """
    if len(password) < 6:
        return False, "Пароль должен содержать минимум 6 символов"
    
    if len(password) > 128:
        return False, "Пароль слишком длинный (максимум 128 символов)"
    
    # Проверяем наличие цифр
    if not any(char.isdigit() for char in password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    
    # Проверяем наличие букв
    if not any(char.isalpha() for char in password):
        return False, "Пароль должен содержать хотя бы одну букву"
    
    return True, "Пароль соответствует требованиям безопасности"
