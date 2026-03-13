from typing import List

import requests

from .config import settings


class NewsClient:
    def __init__(self) -> None:
        self.base_url = settings.news_api_base

    def fetch_related_news(self, query: str, page_size: int = 10) -> List[dict]:
        if not settings.news_api_key:
            return []
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": settings.news_api_key,
        }
        resp = requests.get(f"{self.base_url}/everything", params=params, timeout=20)
        resp.raise_for_status()
        return resp.json().get("articles", [])
