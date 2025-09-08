from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Integer, DateTime, JSON, Boolean
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # Уникальный ник
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)  # Email пользователя
    password_hash: Mapped[str] = mapped_column(String(255))  # Хеш пароля
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # Подтвержден ли email
    uid: Mapped[str | None] = mapped_column(String(128), unique=True, index=True)  # Firebase UID или custom (для совместимости)
    display_name: Mapped[str | None] = mapped_column(String(128))  # Отображаемое имя (для совместимости)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    sessions = relationship("ChatSession", back_populates="user")
    

class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    token: Mapped[str] = mapped_column(String(7))  # 7-значный токен
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    topic: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(32))  # user/ayya/ayana/system
    content: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(128))
    plan: Mapped[dict] = mapped_column(JSON)  # steps, data schema, etc.
    data: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow) 