from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal, Any

Role = Literal["user", "ayya", "ayana", "system"]

class MessageIn(BaseModel):
    role: Role
    content: str

class TurnRequest(BaseModel):
    session_id: Optional[int] = None
    user_uid: str
    topic: Optional[str] = None
    messages: List[MessageIn] = Field(default_factory=list)

class TurnReply(BaseModel):
    role: Literal["ayya", "ayana", "system"]
    say: str
    animations: List[str] = Field(default_factory=list)
    next_task: Optional[str] = None

class CreateSessionRequest(BaseModel):
    user_uid: str
    topic: Optional[str] = None

class CreateSessionReply(BaseModel):
    session_id: int

class ProjectCreateRequest(BaseModel):
    session_id: int
    title: str

class ProjectReply(BaseModel):
    project_id: int
    title: str
    plan: dict 

# Схемы для новой системы авторизации
class UserRegistrationRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Уникальный ник пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    password_confirm: str = Field(..., description="Подтверждение пароля")

class UserLoginRequest(BaseModel):
    username: str = Field(..., description="Ник пользователя")
    password: str = Field(..., description="Пароль пользователя")

class TokenVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    token: str = Field(..., min_length=7, max_length=7, description="7-значный токен подтверждения")

class AuthResponse(BaseModel):
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")
    user_id: int = Field(..., description="ID пользователя в системе")
    username: str = Field(..., description="Ник пользователя")
    email: str = Field(..., description="Email пользователя")
    is_verified: bool = Field(..., description="Подтвержден ли email")

class TokenResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате")
    token_sent: bool = Field(..., description="Отправлен ли токен")
    expires_in: int = Field(..., description="Время жизни токена в секундах")

class UserProfileResponse(BaseModel):
    user_id: int = Field(..., description="ID пользователя в системе")
    username: str = Field(..., description="Ник пользователя")
    email: str = Field(..., description="Email пользователя")
    is_verified: bool = Field(..., description="Подтвержден ли email")
    created_at: str = Field(..., description="Дата создания аккаунта")
    sessions_count: int = Field(..., description="Количество сессий пользователя")

class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., description="Текущий пароль")
    new_password: str = Field(..., min_length=6, description="Новый пароль")
    new_password_confirm: str = Field(..., description="Подтверждение нового пароля")

# Google OAuth схемы (оставляем для совместимости)
class GoogleAuthRequest(BaseModel):
    id_token: str = Field(..., description="Google ID token для аутентификации")

class GoogleAuthResponse(BaseModel):
    access_token: str = Field(..., description="JWT токен приложения")
    token_type: str = Field(default="bearer", description="Тип токена")
    user_id: int = Field(..., description="ID пользователя в системе")
    user_uid: str = Field(..., description="Уникальный идентификатор пользователя")
    display_name: Optional[str] = Field(None, description="Отображаемое имя пользователя")
    email: Optional[str] = Field(None, description="Email пользователя")
    is_new_user: bool = Field(..., description="Новый ли это пользователь") 