import requests

from .config import settings


class TelegramNotifier:
    def send(self, text: str) -> None:
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        payload = {"chat_id": settings.telegram_chat_id, "text": text}
        requests.post(url, json=payload, timeout=15)
