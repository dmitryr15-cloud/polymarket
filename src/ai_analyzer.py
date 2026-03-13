import json
from typing import List

from openai import OpenAI

from .config import settings
from .models import Market, Signal


class AIAnalyzer:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_api_base)

    def analyze_market(self, market: Market, news: List[dict]) -> Signal | None:
        if not news or not settings.openai_api_key:
            return None

        compact_news = [
            {
                "title": n.get("title"),
                "description": n.get("description"),
                "publishedAt": n.get("publishedAt"),
                "source": (n.get("source") or {}).get("name"),
            }
            for n in news[:8]
        ]

        prompt = (
            "You are a risk-aware prediction market analyst. "
            "Estimate fair probability of YES for the market using provided news. "
            "Return strict JSON with keys: fair_prob_yes (0..1), confidence (0..1), reason_short."
        )

        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "market_question": market.question,
                            "market_yes_price": market.yes_price,
                            "news": compact_news,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
        )

        payload = json.loads(completion.choices[0].message.content)
        fair_yes = float(payload["fair_prob_yes"])
        conf = float(payload["confidence"])
        side = "YES" if fair_yes > market.yes_price else "NO"
        return Signal(
            market_id=market.id,
            side=side,
            confidence=conf,
            fair_prob_yes=fair_yes,
            reason=str(payload.get("reason_short", "")),
        )
