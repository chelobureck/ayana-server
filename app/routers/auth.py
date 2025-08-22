from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..db import get_db
from ..models import User, ChatSession, VerificationToken
from ..schemas import (
    UserRegistrationRequest, UserLoginRequest, TokenVerificationRequest,
    AuthResponse, TokenResponse, UserProfileResponse, PasswordChangeRequest
)
from ..email_service import email_service
from ..password_utils import hash_password, verify_password, validate_password_strength
from ..cache import token_cache
from ..config import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register_user(
    registration_data: UserRegistrationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    
    Создает пользователя и отправляет токен подтверждения на email.
    """
    try:
        # Проверяем, что пароли совпадают
        if registration_data.password != registration_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароли не совпадают"
            )
        
        # Проверяем сложность пароля
        is_valid, message = validate_password_strength(registration_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Проверяем, что username не занят
        existing_user = await db.execute(
            select(User).where(User.username == registration_data.username)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким ником уже существует"
            )
        
        # Проверяем, что email не занят
        existing_email = await db.execute(
            select(User).where(User.email == registration_data.email)
        )
        if existing_email.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        
        # Хешируем пароль
        password_hash = hash_password(registration_data.password)
        
        # Создаем пользователя
        new_user = User(
            username=registration_data.username,
            email=registration_data.email,
            password_hash=password_hash,
            is_verified=False
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Генерируем токен подтверждения
        verification_token = email_service.generate_token()
        
        # Сохраняем токен в кэш
        token_cache.store_verification_token(
            registration_data.email,
            verification_token,
            settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
        # Отправляем email с токеном
        email_sent = email_service.send_verification_email(
            registration_data.email,
            verification_token
        )
        
        if not email_sent:
            # Если email не отправлен, удаляем пользователя
            await db.delete(new_user)
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка отправки email. Попробуйте позже."
            )
        
        return TokenResponse(
            message="Пользователь зарегистрирован. Проверьте email для подтверждения.",
            token_sent=True,
            expires_in=settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/verify-email", response_model=AuthResponse)
async def verify_email(
    verification_data: TokenVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Подтверждение email с помощью токена.
    
    После подтверждения пользователь может войти в систему.
    """
    try:
        # Получаем токен из кэша
        cached_token = token_cache.get_verification_token(verification_data.email)
        
        if not cached_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Токен не найден или истек. Запросите новый токен."
            )
        
        # Проверяем токен
        if cached_token != verification_data.token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный токен подтверждения"
            )
        
        # Находим пользователя
        user = await db.execute(
            select(User).where(User.email == verification_data.email)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже подтвержден"
            )
        
        # Подтверждаем email
        user.is_verified = True
        await db.commit()
        await db.refresh(user)
        
        # Удаляем токен из кэша
        token_cache.delete_verification_token(verification_data.email)
        
        # Создаем JWT токен
        token_payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
        }
        
        access_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            username=user.username,
            email=user.email,
            is_verified=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during email verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/login", response_model=AuthResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Вход пользователя по нику и паролю.
    
    Пользователь должен подтвердить email перед входом.
    """
    try:
        # Находим пользователя по нику
        user = await db.execute(
            select(User).where(User.username == login_data.username)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный ник или пароль"
            )
        
        # Проверяем пароль
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный ник или пароль"
            )
        
        # Проверяем, подтвержден ли email
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email не подтвержден. Проверьте email для подтверждения."
            )
        
        # Создаем JWT токен
        token_payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
        }
        
        access_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            username=user.username,
            email=user.email,
            is_verified=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/resend-verification", response_model=TokenResponse)
async def resend_verification_token(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Повторная отправка токена подтверждения.
    
    Полезно, если предыдущий токен истек.
    """
    try:
        # Проверяем, существует ли пользователь
        user = await db.execute(
            select(User).where(User.email == email)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь с таким email не найден"
            )
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже подтвержден"
            )
        
        # Генерируем новый токен
        verification_token = email_service.generate_token()
        
        # Сохраняем токен в кэш
        token_cache.store_verification_token(
            email,
            verification_token,
            settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
        # Отправляем email
        email_sent = email_service.send_verification_email(email, verification_token)
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка отправки email. Попробуйте позже."
            )
        
        return TokenResponse(
            message="Токен подтверждения отправлен на email",
            token_sent=True,
            expires_in=settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resending verification token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/forgot-password", response_model=TokenResponse)
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    """
    Запрос на сброс пароля.
    
    Отправляет токен для сброса пароля на email.
    """
    try:
        # Проверяем, существует ли пользователь
        user = await db.execute(
            select(User).where(User.email == email)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            # Не раскрываем информацию о существовании пользователя
            return TokenResponse(
                message="Если пользователь с таким email существует, токен для сброса пароля отправлен",
                token_sent=True,
                expires_in=settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
            )
        
        # Генерируем токен для сброса пароля
        reset_token = email_service.generate_token()
        
        # Сохраняем токен в кэш
        token_cache.store_password_reset_token(
            email,
            reset_token,
            settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
        # Отправляем email
        email_sent = email_service.send_password_reset_email(email, reset_token)
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка отправки email. Попробуйте позже."
            )
        
        return TokenResponse(
            message="Токен для сброса пароля отправлен на email",
            token_sent=True,
            expires_in=settings.VERIFICATION_TOKEN_EXPIRE_SECONDS
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during forgot password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/reset-password")
async def reset_password(
    email: str,
    token: str,
    new_password: str,
    new_password_confirm: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Сброс пароля с помощью токена.
    """
    try:
        # Проверяем, что пароли совпадают
        if new_password != new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароли не совпадают"
            )
        
        # Проверяем сложность пароля
        is_valid, message = validate_password_strength(new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Получаем токен из кэша
        cached_token = token_cache.get_password_reset_token(email)
        
        if not cached_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Токен не найден или истек. Запросите новый токен."
            )
        
        # Проверяем токен
        if cached_token != token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный токен для сброса пароля"
            )
        
        # Находим пользователя
        user = await db.execute(
            select(User).where(User.email == email)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        # Обновляем пароль
        user.password_hash = hash_password(new_password)
        await db.commit()
        
        # Удаляем токен из кэша
        token_cache.delete_password_reset_token(email)
        
        return {"message": "Пароль успешно изменен"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during password reset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: dict = Depends(lambda x: x),  # Будет заменено на реальную аутентификацию
    db: AsyncSession = Depends(get_db)
):
    """
    Изменение пароля авторизованным пользователем.
    """
    try:
        # TODO: Добавить реальную аутентификацию
        # Пока что это заглушка
        
        # Проверяем, что новые пароли совпадают
        if password_data.new_password != password_data.new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Новые пароли не совпадают"
            )
        
        # Проверяем сложность нового пароля
        is_valid, message = validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # TODO: Получить реального пользователя из токена
        # user = await get_current_user(current_user, db)
        
        # TODO: Проверить текущий пароль
        # if not verify_password(password_data.current_password, user.password_hash):
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Неверный текущий пароль"
        #     )
        
        # TODO: Обновить пароль
        # user.password_hash = hash_password(password_data.new_password)
        # await db.commit()
        
        return {"message": "Пароль успешно изменен"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during password change: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: dict = Depends(lambda x: x),  # Будет заменено на реальную аутентификацию
    db: AsyncSession = Depends(get_db)
):
    """
    Получение профиля пользователя.
    """
    try:
        # TODO: Добавить реальную аутентификацию
        # user = await get_current_user(current_user, db)
        
        # Подсчет количества сессий
        # sessions_count = await db.scalar(
        #     select(func.count(ChatSession.id)).where(ChatSession.user_id == user.id)
        # )
        
        # return UserProfileResponse(
        #     user_id=user.id,
        #     username=user.username,
        #     email=user.email,
        #     is_verified=user.is_verified,
        #     created_at=user.created_at.isoformat(),
        #     sessions_count=sessions_count or 0
        # )
        
        # Временная заглушка
        return UserProfileResponse(
            user_id=1,
            username="test_user",
            email="test@example.com",
            is_verified=True,
            created_at=datetime.utcnow().isoformat(),
            sessions_count=0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

# Оставляем Google OAuth для совместимости
@router.post("/google")
async def login_with_google(
    id_token_str: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация через Google OAuth (для совместимости).
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_CLIENT_ID не настроен в конфигурации"
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        
        if idinfo.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
            raise ValueError("Неверный издатель токена")
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Недействительный Google ID token: {str(e)}"
        )

    google_sub = idinfo.get("sub")
    email = idinfo.get("email")
    name = idinfo.get("name")
    
    if not google_sub:
        raise HTTPException(
            status_code=401,
            detail="Неверная структура Google токена"
        )

    uid = f"google:{google_sub}"

    q = await db.execute(select(User).where(User.uid == uid))
    user = q.scalar_one_or_none()
    
    if user is None:
        user = User(
            uid=uid,
            username=name or email,
            email=email,
            display_name=name or email,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token_payload = {
        "uid": uid,
        "user_id": user.id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    }
    
    app_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    return {
        "access_token": app_token,
        "token_type": "bearer",
        "user_id": user.id
    }