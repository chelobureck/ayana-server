import smtplib
import random
import string
import requests
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .config import settings
from .cache import redis_client
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.refresh_token = settings.GOOGLE_REFRESH_TOKEN

    def _get_access_token(self) -> str:
        """Получает новый access_token через refresh_token"""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def generate_token(self) -> str:
        """Генерирует 7-значный токен"""
        return ''.join(random.choices(string.digits, k=settings.VERIFICATION_TOKEN_LENGTH))

    def _send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        """Отправка письма через Gmail XOAUTH2"""
        try:
            # Собираем письмо
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_body, "html"))

            # Получаем свежий access_token
            access_token = self._get_access_token()

            # Формируем XOAUTH2 строку
            auth_string = f"user={self.smtp_user}\1auth=Bearer {access_token}\1\1"
            auth_bytes = base64.b64encode(auth_string.encode("utf-8"))

            # SMTP подключение
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.docmd("AUTH", "XOAUTH2 " + auth_bytes.decode("utf-8"))

            # Отправляем письмо
            server.sendmail(self.smtp_user, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_verification_email(self, email: str, token: str) -> bool:
        """Отправляет email с токеном подтверждения"""
        html_body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">Ayana AI - Подтверждение email</h2>
                <p>Для подтверждения вашего email используйте следующий токен:</p>
                <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                    <h1 style="color: #667eea; font-size: 32px; letter-spacing: 5px; margin: 0;">{token}</h1>
                </div>
                <p><strong>Внимание:</strong> Токен действителен только <strong>45 секунд</strong>!</p>
                <p>Если вы не регистрировались, проигнорируйте это письмо.</p>
            </div>
        </body>
        </html>
        """
        return self._send_email(email, "Ayana AI - Подтверждение email", html_body)

    def send_password_reset_email(self, email: str, token: str) -> bool:
        """Отправляет email для сброса пароля"""
        html_body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">Ayana AI - Сброс пароля</h2>
                <p>Для сброса пароля используйте следующий токен:</p>
                <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                    <h1 style="color: #667eea; font-size: 32px; letter-spacing: 5px; margin: 0;">{token}</h1>
                </div>
                <p><strong>Внимание:</strong> Токен действителен только <strong>45 секунд</strong>!</p>
                <p>Если вы не запрашивали сброс пароля, просто проигнорируйте письмо.</p>
            </div>
        </body>
        </html>
        """
        return self._send_email(email, "Ayana AI - Сброс пароля", html_body)

# Глобальный экземпляр
email_service = EmailService()
