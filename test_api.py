#!/usr/bin/env python3
"""
Тестирование API AI Tutor Server
Запуск: python test_api.py
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_health():
    """Тест health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"✅ Health: {response.status_code} - {response.json()}")

async def test_auth():
    """Тест аутентификации"""
    async with httpx.AsyncClient() as client:
        # Создание пользователя
        response = await client.post(
            f"{BASE_URL}/auth/ensure-user",
            params={"uid": "demo123", "display_name": "Тестовый ребенок"}
        )
        print(f"✅ Auth ensure-user: {response.status_code} - {response.json()}")

async def test_lesson():
    """Тест уроков"""
    async with httpx.AsyncClient() as client:
        # Создание сессии
        response = await client.post(
            f"{BASE_URL}/lesson/create-session",
            json={"user_uid": "demo123", "topic": "Математика для малышей"}
        )
        print(f"✅ Create session: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            
            # Тест диалога
            turn_response = await client.post(
                f"{BASE_URL}/lesson/turn",
                json={
                    "user_uid": "demo123",
                    "session_id": session_id,
                    "messages": [
                        {"role": "user", "content": "Почему 2+2=4?"}
                    ]
                }
            )
            print(f"✅ Lesson turn: {turn_response.status_code}")
            if turn_response.status_code == 200:
                turn_data = turn_response.json()
                print(f"   Role: {turn_data.get('role')}")
                print(f"   Say: {turn_data.get('say')[:100]}...")
                print(f"   Animations: {turn_data.get('animations')}")

async def test_project():
    """Тест проектов"""
    async with httpx.AsyncClient() as client:
        # Сначала создаем сессию
        session_response = await client.post(
            f"{BASE_URL}/lesson/create-session",
            json={"user_uid": "demo123", "topic": "Проект"}
        )
        
        if session_response.status_code == 200:
            session_id = session_response.json()["session_id"]
            
            # Создание проекта
            project_response = await client.post(
                f"{BASE_URL}/project/create",
                json={"session_id": session_id, "title": "Мой первый проект"}
            )
            print(f"✅ Create project: {project_response.status_code} - {project_response.json()}")

async def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование AI Tutor Server API")
    print("=" * 50)
    
    try:
        await test_health()
        await test_auth()
        await test_lesson()
        await test_project()
        
        print("\n🎉 Все тесты завершены!")
        
    except httpx.ConnectError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 