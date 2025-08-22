#!/usr/bin/env python3
"""
Тестирование Google OAuth API
"""

import requests
import json
import os
from typing import Optional

class GoogleOAuthTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        
    def test_google_auth(self, google_id_token: str) -> bool:
        """
        Тестирование аутентификации через Google
        
        Args:
            google_id_token: Google ID token для тестирования
            
        Returns:
            bool: True если тест прошел успешно
        """
        print("🔐 Тестирование Google OAuth аутентификации...")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/google",
                json={"id_token": google_id_token},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                
                print("✅ Аутентификация успешна!")
                print(f"   User ID: {data['user_id']}")
                print(f"   User UID: {data['user_uid']}")
                print(f"   Display Name: {data['display_name']}")
                print(f"   Email: {data['email']}")
                print(f"   Новый пользователь: {'Да' if data['is_new_user'] else 'Нет'}")
                
                return True
            else:
                print(f"❌ Ошибка аутентификации: {response.status_code}")
                print(f"   Детали: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def test_get_profile(self) -> bool:
        """
        Тестирование получения профиля пользователя
        
        Returns:
            bool: True если тест прошел успешно
        """
        if not self.access_token:
            print("❌ Нет access token для тестирования профиля")
            return False
            
        print("\n👤 Тестирование получения профиля пользователя...")
        
        try:
            response = requests.get(
                f"{self.base_url}/auth/profile",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                profile = response.json()
                print("✅ Профиль получен успешно!")
                print(f"   User ID: {profile['user_id']}")
                print(f"   User UID: {profile['user_uid']}")
                print(f"   Display Name: {profile['display_name']}")
                print(f"   Email: {profile['email']}")
                print(f"   Дата создания: {profile['created_at']}")
                print(f"   Количество сессий: {profile['sessions_count']}")
                
                return True
            else:
                print(f"❌ Ошибка получения профиля: {response.status_code}")
                print(f"   Детали: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def test_refresh_token(self) -> bool:
        """
        Тестирование обновления токена
        
        Returns:
            bool: True если тест прошел успешно
        """
        if not self.access_token:
            print("❌ Нет access token для тестирования обновления")
            return False
            
        print("\n🔄 Тестирование обновления токена...")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/refresh",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                old_token = self.access_token
                self.access_token = data['access_token']
                
                print("✅ Токен обновлен успешно!")
                print(f"   Новый токен: {self.access_token[:20]}...")
                print(f"   Время жизни: {data['expires_in']} секунд")
                
                # Проверяем, что новый токен отличается от старого
                if old_token != self.access_token:
                    print("   ✅ Новый токен отличается от старого")
                else:
                    print("   ⚠️  Новый токен совпадает со старым")
                
                return True
            else:
                print(f"❌ Ошибка обновления токена: {response.status_code}")
                print(f"   Детали: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def test_invalid_token(self) -> bool:
        """
        Тестирование обработки недействительного токена
        
        Returns:
            bool: True если тест прошел успешно (ошибка обработана корректно)
        """
        print("\n🚫 Тестирование обработки недействительного токена...")
        
        try:
            response = requests.get(
                f"{self.base_url}/auth/profile",
                headers={"Authorization": "Bearer invalid_token_here"},
                timeout=10
            )
            
            if response.status_code == 401:
                print("✅ Недействительный токен корректно отклонен")
                return True
            else:
                print(f"❌ Неожиданный статус код: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def run_all_tests(self, google_id_token: str) -> bool:
        """
        Запуск всех тестов
        
        Args:
            google_id_token: Google ID token для тестирования
            
        Returns:
            bool: True если все тесты прошли успешно
        """
        print("🚀 Запуск тестов Google OAuth API")
        print("=" * 50)
        
        tests = [
            ("Google OAuth", lambda: self.test_google_auth(google_id_token)),
            ("Получение профиля", self.test_get_profile),
            ("Обновление токена", self.test_refresh_token),
            ("Проверка недействительного токена", self.test_invalid_token),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Ошибка в тесте '{test_name}': {e}")
                results.append((test_name, False))
        
        print("\n" + "=" * 50)
        print("📊 Результаты тестов:")
        
        passed = 0
        for test_name, result in results:
            status = "✅ ПРОШЕЛ" if result else "❌ ПРОВАЛЕН"
            print(f"   {test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Итого: {passed}/{len(results)} тестов прошли успешно")
        
        return passed == len(results)

def main():
    """Основная функция"""
    print("🧪 Тестирование Google OAuth API")
    print("=" * 50)
    
    # Получение Google ID token из переменной окружения или пользователя
    google_id_token = os.getenv("GOOGLE_ID_TOKEN")
    
    if not google_id_token:
        print("⚠️  Переменная окружения GOOGLE_ID_TOKEN не установлена")
        print("   Установите её или введите токен вручную")
        google_id_token = input("Введите Google ID token для тестирования: ").strip()
        
        if not google_id_token:
            print("❌ Google ID token не предоставлен. Завершение работы.")
            return
    
    # Создание тестера и запуск тестов
    tester = GoogleOAuthTester()
    success = tester.run_all_tests(google_id_token)
    
    if success:
        print("\n🎉 Все тесты прошли успешно!")
    else:
        print("\n💥 Некоторые тесты не прошли. Проверьте логи выше.")

if __name__ == "__main__":
    main()
