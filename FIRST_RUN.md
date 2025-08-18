# 🚀 Первый запуск AI Tutor Server

## 🎯 Пошаговое руководство для новичков

### Шаг 1: Проверка требований ✅

Убедитесь что у вас установлено:
```bash
# Docker Desktop
docker --version
# Должен показать версию Docker

# Git (опционально, для клонирования)
git --version
```

**Если Docker не установлен:**
- Windows: [Docker Desktop для Windows](https://docs.docker.com/desktop/install/windows-install/)
- Mac: [Docker Desktop для Mac](https://docs.docker.com/desktop/install/mac-install/)
- Linux: [Docker Engine для Linux](https://docs.docker.com/engine/install/)

### Шаг 2: Подготовка проекта 📁

```bash
# Если у вас есть архив - распакуйте его
# Если клонируете из Git:
git clone <your-repo-url>
cd ai-tutor-server

# Убедитесь что все файлы на месте
ls -la
# Должны быть: app/, docker-compose.yml, Dockerfile, start.bat, start.sh и др.
```

### Шаг 3: Настройка конфигурации ⚙️

```bash
# Скопируйте пример конфигурации
cp env.example .env

# Откройте .env файл в любом текстовом редакторе
# Windows: notepad .env
# Mac/Linux: nano .env или code .env
```

**В .env файле ОБЯЗАТЕЛЬНО заполните:**
```bash
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

**Где взять API ключ:**
1. Зайдите на [OpenRouter](https://openrouter.ai/)
2. Создайте аккаунт
3. Получите API ключ в разделе API Keys
4. Вставьте ключ в .env файл

### Шаг 4: Запуск сервера 🐳

#### Windows:
```bash
# Двойной клик на start.bat
# Или в командной строке:
start.bat
```

#### Mac/Linux:
```bash
# Сделайте скрипт исполняемым
chmod +x start.sh

# Запустите
./start.sh
```

#### Ручной запуск:
```bash
docker compose up --build
```

**Что происходит:**
1. Docker скачивает образы PostgreSQL и Redis
2. Собирает Python приложение
3. Создает базу данных
4. Запускает все сервисы

**Первый запуск может занять 5-10 минут!**

### Шаг 5: Проверка работы ✅

Откройте новое окно терминала и выполните:

```bash
# Проверка здоровья сервиса
curl http://localhost:8000/health

# Должен вернуть: {"ok": true}
```

**Если curl не работает:**
- Windows: установите [Git Bash](https://git-scm.com/download/win) или используйте PowerShell
- Mac: curl должен быть установлен по умолчанию
- Linux: `sudo apt install curl` (Ubuntu/Debian)

### Шаг 6: Тестирование API 🧪

```bash
# Автоматическое тестирование
python test_api.py

# Или ручное тестирование
curl -X POST "http://localhost:8000/auth/ensure-user?uid=demo123&display_name=Kid"
```

## 🚨 Решение проблем

### Проблема: Docker не запускается
```bash
# Проверьте что Docker Desktop запущен
# В Windows: иконка Docker в трее
# В Mac: Docker Desktop приложение

# Перезапустите Docker Desktop
# Очистите контейнеры
docker compose down -v
docker compose up --build
```

### Проблема: Порты заняты
```bash
# Проверьте что порты свободны
netstat -an | grep :8000
netstat -an | grep :5432
netstat -an | grep :6379

# Если заняты, остановите другие сервисы или измените порты в docker-compose.yml
```

### Проблема: База данных не подключается
```bash
# Проверьте логи
docker compose logs postgres

# Перезапустите PostgreSQL
docker compose restart postgres
```

### Проблема: API не отвечает
```bash
# Проверьте .env файл
cat .env | grep OPENAI

# Проверьте логи API
docker compose logs api

# Убедитесь что API ключ правильный
```

## 🎉 Успешный запуск!

Если вы видите:
```bash
{"ok": true}
```

**Поздравляем! 🎉 Ваш AI Tutor Server работает!**

## 📱 Следующие шаги

1. **Интегрируйте с Flutter** - читайте `flutter_integration.md`
2. **Протестируйте диалоги** - используйте `curl_examples.md`
3. **Деплой на продакшен** - следуйте `deploy_guide.md`

## 🔧 Полезные команды

```bash
# Статус всех сервисов
docker compose ps

# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redis

# Остановка сервисов
docker compose down

# Перезапуск
docker compose restart

# Обновление и перезапуск
docker compose down
docker compose up --build
```

## 📚 Документация

- **`START_HERE.md`** - главный файл для начала
- **`QUICKSTART.md`** - быстрый старт за 5 минут
- **`CHECKLIST.md`** - чек-лист готовности
- **`flutter_integration.md`** - интеграция с Flutter

---

## 🆘 Нужна помощь?

1. Проверьте логи: `docker compose logs -f`
2. Убедитесь что все сервисы запущены: `docker compose ps`
3. Проверьте переменные окружения: `docker compose exec api env`
4. Создайте issue в репозитории

**Удачи с вашим AI Tutor Server! 🚀** 