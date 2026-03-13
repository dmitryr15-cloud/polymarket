from __future__ import annotations

from datetime import datetime, timezone
from typing import List

import requests

from .config import settings
from .models import Market, Position


class PolymarketClient:
    def __init__(self) -> None:
        self.base_url = settings.polymarket_api_base
        self.session = requests.Session()
        if settings.polymarket_api_key:
            self.session.headers.update({"Authorization": f"Bearer {settings.polymarket_api_key}"})

    def get_markets(self) -> List[Market]:
        # NOTE: endpoint shape may vary, this is a safe starter pattern.
        url = f"{self.base_url}/markets"
        resp = self.session.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        markets: List[Market] = []
        for item in data[:200]:
            try:
                close_time = datetime.fromisoformat(item.get("endDate", "1970-01-01T00:00:00+00:00"))
            except ValueError:
                close_time = datetime.now(timezone.utc)

            markets.append(
                Market(
                    id=str(item.get("id", "")),
                    question=item.get("question", ""),
                    yes_price=float(item.get("yesPrice", 0.5)),
                    no_price=float(item.get("noPrice", 0.5)),
                    liquidity_usd=float(item.get("liquidity", 0.0)),
                    close_time=close_time,
                )
            )
        return markets

    def get_open_positions(self) -> List[Position]:
        # Starter placeholder; adapt to account endpoint.
        return []

    def place_order(self, market_id: str, side: str, size_usd: float, limit_price: float) -> dict:
        payload = {
            "market_id": market_id,
            "side": side,
            "size_usd": size_usd,
            "limit_price": limit_price,
        }
        if settings.dry_run:
            return {"status": "dry_run", "payload": payload}

        url = f"{self.base_url}/orders"
        resp = self.session.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        return resp.json()

    def close_position(self, position: Position) -> dict:
        opposite_side = "NO" if position.side == "YES" else "YES"
        return self.place_order(
            market_id=position.market_id,
            side=opposite_side,
            size_usd=position.size_usd,
            limit_price=0.5,
        )
