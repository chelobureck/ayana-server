import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from .config import settings
from .cache import redis_client
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        
    def generate_token(self) -> str:
        """Генерирует 7-значный токен"""
        return ''.join(random.choices(string.digits, k=settings.VERIFICATION_TOKEN_LENGTH))
    
    def send_verification_email(self, email: str, token: str) -> bool:
        """Отправляет email с токеном подтверждения"""
        try:
            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = email
            msg['Subject'] = "Ayana AI - Подтверждение email"
            
            # HTML тело письма
            html_body = f"""
            <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #667eea;">Ayana AI - Подтверждение email</h2>
                    <p>Здравствуйте!</p>
                    <p>Для подтверждения вашего email адреса используйте следующий токен:</p>
                    <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                        <h1 style="color: #667eea; font-size: 32px; letter-spacing: 5px; margin: 0;">{token}</h1>
                    </div>
                    <p><strong>Внимание:</strong> Токен действителен только <strong>45 секунд</strong>!</p>
                    <p>Если вы не регистрировались в Ayana AI, просто проигнорируйте это письмо.</p>
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 12px;">
                        Это автоматическое сообщение, не отвечайте на него.
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Подключаемся к SMTP серверу
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_tls:
                server.starttls()
            
            # Авторизуемся
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            
            # Отправляем письмо
            text = msg.as_string()
            server.sendmail(self.smtp_user, email, text)
            server.quit()
            
            logger.info(f"Verification email sent to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            return False
    
    def send_password_reset_email(self, email: str, token: str) -> bool:
        """Отправляет email для сброса пароля"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = email
            msg['Subject'] = "Ayana AI - Сброс пароля"
            
            html_body = f"""
            <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #667eea;">Ayana AI - Сброс пароля</h2>
                    <p>Здравствуйте!</p>
                    <p>Для сброса пароля используйте следующий токен:</p>
                    <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                        <h1 style="color: #667eea; font-size: 32px; letter-spacing: 5px; margin: 0;">{token}</h1>
                    </div>
                    <p><strong>Внимание:</strong> Токен действителен только <strong>45 секунд</strong>!</p>
                    <p>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 12px;">
                        Это автоматическое сообщение, не отвечайте на него.
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_tls:
                server.starttls()
            
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            
            text = msg.as_string()
            server.sendmail(self.smtp_user, email, text)
            server.quit()
            
            logger.info(f"Password reset email sent to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False

# Создаем глобальный экземпляр сервиса
email_service = EmailService()
