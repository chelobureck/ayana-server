# 📖 Руководство по использованию AI Tutor Server

## 🎯 Основные концепции

### AI Оркестрация
AI Tutor Server использует **две роли** для создания интерактивного образовательного опыта:

1. **Айя** - добрый учитель
   - Объясняет темы простыми словами
   - Использует примеры из жизни
   - Дает мягкие исправления
   - Описывает анимации для показа

2. **Аяна** - одноклассница
   - Задает уточняющие вопросы
   - Ведет к мини-проектам
   - Углубляет понимание
   - Создает практические задания

### Техника Фейнмана
Образовательный процесс следует принципу:
```
Объяснение → Вопросы → Исправления → Мини-проект
```

## 🚀 API Endpoints

### 1. Проверка здоровья
```bash
GET /health
```
**Ответ:**
```json
{"ok": true}
```

### 2. Создание/получение пользователя
```bash
POST /auth/ensure-user?uid={uid}&display_name={name}
```
**Параметры:**
- `uid` (обязательно) - уникальный идентификатор пользователя
- `display_name` (опционально) - отображаемое имя

**Ответ:**
```json
{"user_id": 1}
```

### 3. Создание сессии урока
```bash
POST /lesson/create-session
```
**Тело запроса:**
```json
{
  "user_uid": "demo123",
  "topic": "Математика для малышей"
}
```
**Ответ:**
```json
{"session_id": 1}
```

### 4. Диалог с AI (ОСНОВНОЙ ENDPOINT)
```bash
POST /lesson/turn
```
**Тело запроса:**
```json
{
  "user_uid": "demo123",
  "session_id": 1,
  "topic": "Сложение",
  "messages": [
    {
      "role": "user",
      "content": "Почему 2+2=4?"
    }
  ]
}
```

**Ответ:**
```json
{
  "role": "ayya",
  "say": "Представь, что у тебя есть 2 яблока, и мама дала еще 2. Сколько всего яблок?",
  "animations": ["яблоки появляются", "счет 1-2-3-4"],
  "next_task": "Попробуй сосчитать свои игрушки!"
}
```

### 5. Создание проекта
```bash
POST /project/create
```
**Тело запроса:**
```json
{
  "session_id": 1,
  "title": "Мой первый математический проект"
}
```

**Ответ:**
```json
{
  "project_id": 1,
  "title": "Мой первый математический проект",
  "plan": {
    "steps": [
      "Соберём 10 наблюдений (сосчитай яблоки/игрушки)",
      "Сделаем таблицу: что и сколько получилось",
      "Соберём мини-презентацию (3 слайда) для родителей"
    ],
    "data_schema": {"item": "string", "count": "int"}
  }
}
```

## 💬 Примеры диалогов

### Простой вопрос
```
Ребенок: "Почему небо голубое?"
Айя: "Представь, что солнце - это большой фонарик. Когда его свет проходит через воздух, он рассеивается, как вода в стакане. Голубой цвет рассеивается больше всего, поэтому мы видим голубое небо!"
```

### Уточняющий вопрос от Аяны
```
Ребенок: "Понял!"
Аяна: "А если бы не было воздуха, какого цвета было бы небо?"
```

### Исправление ошибки
```
Ребенок: "Небо черное ночью!"
Айя: "Хороший вопрос! Ночью солнце не светит на нашу сторону Земли, поэтому мы не видим рассеянный свет. Но если посмотреть в телескоп, можно увидеть звезды - они тоже светят!"
```

## 🎨 Анимации

LLM описывает простые анимации для показа на экране:

### Примеры анимаций:
- `"шарик летит вверх"` - анимировать движение шарика
- `"яблоки исчезают"` - показать исчезновение объектов
- `"счет 1-2-3-4"` - анимировать счет
- `"цвета меняются"` - переход между цветами
- `"геометрические фигуры появляются"` - появление фигур

### Реализация в Flutter:
```dart
void showAnimation(String animation) {
  switch (animation) {
    case "шарик летит вверх":
      // Анимация движения шарика
      break;
    case "яблоки исчезают":
      // Анимация исчезновения
      break;
    // ... другие анимации
  }
}
```

## 📱 Интеграция с Flutter

### Настройка HTTP клиента
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  static Future<TurnReply> lessonTurn({
    required String userUid,
    int? sessionId,
    String? topic,
    required List<Message> messages,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/lesson/turn'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_uid': userUid,
        'session_id': sessionId,
        'topic': topic,
        'messages': messages.map((m) => m.toJson()).toList(),
      }),
    );
    
    if (response.statusCode == 200) {
      return TurnReply.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to get AI response');
    }
  }
}
```

### Модели данных
```dart
class Message {
  final String role;
  final String content;
  
  Message({required this.role, required this.content});
  
  Map<String, dynamic> toJson() => {
    'role': role,
    'content': content,
  };
  
  factory Message.fromJson(Map<String, dynamic> json) => Message(
    role: json['role'],
    content: json['content'],
  );
}

class TurnReply {
  final String role;
  final String say;
  final List<String> animations;
  final String? nextTask;
  
  TurnReply({
    required this.role,
    required this.say,
    required this.animations,
    this.nextTask,
  });
  
  factory TurnReply.fromJson(Map<String, dynamic> json) => TurnReply(
    role: json['role'],
    say: json['say'],
    animations: List<String>.from(json['animations'] ?? []),
    nextTask: json['next_task'],
  );
}
```

### Пример UI для чата
```dart
class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Message> messages = [];
  final TextEditingController _controller = TextEditingController();
  int? sessionId;
  bool isLoading = false;
  
  @override
  void initState() {
    super.initState();
    _initializeSession();
  }
  
  Future<void> _initializeSession() async {
    try {
      final session = await ApiService.createSession('demo123', topic: 'Математика');
      setState(() {
        sessionId = session['session_id'];
      });
    } catch (e) {
      print('Error creating session: $e');
    }
  }
  
  Future<void> _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;
    
    final userMessage = Message(role: 'user', content: _controller.text.trim());
    setState(() {
      messages.add(userMessage);
      isLoading = true;
    });
    _controller.clear();
    
    try {
      final reply = await ApiService.lessonTurn(
        userUid: 'demo123',
        sessionId: sessionId,
        messages: messages,
      );
      
      setState(() {
        messages.add(Message(role: reply.role, content: reply.say));
        isLoading = false;
      });
      
      // Показать анимации
      if (reply.animations.isNotEmpty) {
        _showAnimations(reply.animations);
      }
      
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      print('Error getting AI response: $e');
    }
  }
  
  void _showAnimations(List<String> animations) {
    // Показать анимации в UI
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Анимации: ${animations.join(', ')}')),
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Репетитор')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final message = messages[index];
                return ListTile(
                  title: Text(message.content),
                  subtitle: Text(message.role),
                  leading: Icon(_getRoleIcon(message.role)),
                );
              },
            ),
          ),
          if (isLoading)
            Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Введите сообщение...',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  IconData _getRoleIcon(String role) {
    switch (role) {
      case 'user':
        return Icons.person;
      case 'ayya':
        return Icons.school;
      case 'ayana':
        return Icons.child_care;
      default:
        return Icons.chat;
    }
  }
}
```

## 🔐 Аутентификация

### Разработка
В режиме разработки можно передавать UID напрямую:
```dart
// Простая аутентификация для разработки
final userUid = "demo123";
```

### Продакшен
Для продакшена используйте JWT токены:
```dart
class AuthService {
  static String? _token;
  
  static void setToken(String token) {
    _token = token;
  }
  
  static Map<String, String> get authHeaders => {
    'Content-Type': 'application/json',
    if (_token != null) 'Authorization': 'Bearer $_token',
  };
}

// Использование в API запросах
headers: AuthService.authHeaders,
```

## 🌐 CORS и веб-версия

### Настройка CORS
В `app/config.py` для продакшена:
```python
APP_CORS_ORIGINS = "https://yourdomain.com,https://app.yourdomain.com"
```

### Веб-версия Flutter
Если планируете веб-версию, убедитесь что CORS настроен правильно.

## 🧪 Тестирование

### Автоматическое тестирование
```bash
python test_api.py
```

### Ручное тестирование
```bash
# Создание пользователя
curl -X POST "http://localhost:8000/auth/ensure-user?uid=demo123&display_name=Kid"

# Диалог с AI
curl -X POST http://localhost:8000/lesson/turn \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid":"demo123",
    "messages":[{"role":"user","content":"Почему 2+2=4?"}]
  }'
```

## 🚨 Обработка ошибок

### HTTP ошибки
```dart
try {
  final response = await ApiService.lessonTurn(...);
  // Обработка успешного ответа
} catch (e) {
  if (e.toString().contains('401')) {
    // Ошибка аутентификации
    _showLoginDialog();
  } else if (e.toString().contains('500')) {
    // Ошибка сервера
    _showErrorDialog('Сервер временно недоступен');
  } else {
    // Общая ошибка
    _showErrorDialog('Произошла ошибка: $e');
  }
}
```

### Валидация данных
```dart
// Проверка обязательных полей
if (userUid.isEmpty) {
  throw Exception('User UID is required');
}

if (messages.isEmpty) {
  throw Exception('At least one message is required');
}
```

## 💡 Лучшие практики

### 1. Кеширование
- Используйте Redis кеш для экономии API вызовов
- Кешируйте часто используемые ответы

### 2. Обработка ошибок
- Всегда обрабатывайте HTTP ошибки
- Показывайте понятные сообщения пользователю

### 3. Анимации
- Реализуйте простые анимации для лучшего UX
- Используйте описания от LLM как инструкции

### 4. Безопасность
- Валидируйте все входные данные
- Используйте HTTPS в продакшене
- Настройте правильные CORS заголовки

## 🎯 Следующие шаги

1. **Протестируйте API** - используйте `test_api.py`
2. **Интегрируйте с Flutter** - следуйте примерам выше
3. **Настройте анимации** - реализуйте простые анимации
4. **Деплой на продакшен** - используйте `deploy_guide.md`

---

## 🆘 Нужна помощь?

1. Проверьте логи: `docker compose logs -f`
2. Убедитесь что все сервисы запущены: `docker compose ps`
3. Протестируйте API: `python test_api.py`
4. Создайте issue в репозитории

**Удачи с интеграцией! 🚀** 