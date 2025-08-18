# 📱 Интеграция с Flutter

## 🔗 Настройка базового URL

В вашем Flutter приложении создайте константу для API:

```dart
class ApiConfig {
  // Для локальной разработки
  static const String baseUrl = 'http://localhost:8000';
  
  // Для тестирования на устройстве (замените на ваш IP)
  // static const String baseUrl = 'http://192.168.1.100:8000';
  
  // Для продакшена (Render)
  // static const String baseUrl = 'https://your-app.onrender.com';
}
```

## 🚀 HTTP клиент

Используйте `http` или `dio` пакет для HTTP запросов:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = ApiConfig.baseUrl;
  
  // Создание пользователя
  static Future<Map<String, dynamic>> ensureUser(String uid, {String? displayName}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/ensure-user?uid=$uid&display_name=${displayName ?? ''}'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to ensure user');
    }
  }
  
  // Создание сессии
  static Future<Map<String, dynamic>> createSession(String userUid, {String? topic}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/lesson/create-session'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_uid': userUid,
        'topic': topic,
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to create session');
    }
  }
  
  // Диалог с AI
  static Future<Map<String, dynamic>> lessonTurn({
    required String userUid,
    int? sessionId,
    String? topic,
    required List<Map<String, String>> messages,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/lesson/turn'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_uid': userUid,
        'session_id': sessionId,
        'topic': topic,
        'messages': messages,
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to get AI response');
    }
  }
}
```

## 🎯 Модели данных

Создайте модели для работы с API:

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

## 💬 Пример использования в UI

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
        messages: messages.map((m) => m.toJson()).toList(),
      );
      
      final aiMessage = TurnReply.fromJson(reply);
      setState(() {
        messages.add(Message(role: aiMessage.role, content: aiMessage.say));
        isLoading = false;
      });
      
      // Показать анимации
      if (aiMessage.animations.isNotEmpty) {
        _showAnimations(aiMessage.animations);
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

Для продакшена настройте JWT токены:

```dart
class AuthService {
  static String? _token;
  
  static String? get token => _token;
  
  static void setToken(String token) {
    _token = token;
  }
  
  static Map<String, String> get authHeaders => {
    'Content-Type': 'application/json',
    if (_token != null) 'Authorization': 'Bearer $_token',
  };
}

// Использование в API запросах:
headers: AuthService.authHeaders,
```

## 🌐 CORS для веб-версии

Если планируете веб-версию Flutter, убедитесь что CORS настроен правильно в `app/config.py`:

```python
APP_CORS_ORIGINS = "http://localhost:3000,https://yourdomain.com"
```

## 📱 Тестирование на устройстве

1. Запустите сервер: `docker compose up --build`
2. Найдите ваш локальный IP: `ipconfig` (Windows) или `ifconfig` (Mac/Linux)
3. В Flutter измените `baseUrl` на ваш IP: `http://192.168.1.100:8000`
4. Убедитесь что устройство в той же сети

## 🚀 Готовые примеры

Полные примеры интеграции смотрите в:
- `test_api.py` - Python тесты
- `curl_examples.md` - cURL команды
- `README.md` - общая документация 