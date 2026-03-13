from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, List

from .config import settings
from .models import Market, Position, Signal


class Strategy:
    def pick_markets(self, markets: Iterable[Market]) -> List[Market]:
        now = datetime.now(timezone.utc)
        chosen: List[Market] = []
        for m in markets:
            if m.liquidity_usd < settings.min_liquidity:
                continue
            if (m.close_time - now) < timedelta(hours=2):
                continue
            spread = abs(1 - (m.yes_price + m.no_price))
            spread_bps = spread * 10000
            if spread_bps > settings.max_spread_bps:
                continue
            chosen.append(m)
        return chosen[:25]

    def should_open(self, market: Market, signal: Signal, open_positions: List[Position]) -> bool:
        if len(open_positions) >= settings.max_open_positions:
            return False

        edge = signal.fair_prob_yes - market.yes_price
        if signal.side == "NO":
            edge = market.yes_price - signal.fair_prob_yes

        return edge >= settings.min_edge_to_open and signal.confidence >= 0.55

    def should_close(self, position: Position, current_yes_price: float) -> bool:
        now = datetime.now(timezone.utc)
        age_min = (now - position.opened_at).total_seconds() / 60
        if age_min > settings.max_position_lifetime_min:
            return True

        if position.side == "YES":
            pnl_pct = (current_yes_price - position.entry_price) / max(position.entry_price, 1e-6)
        else:
            pnl_pct = ((1 - current_yes_price) - (1 - position.entry_price)) / max((1 - position.entry_price), 1e-6)

        return pnl_pct <= -settings.stop_loss_pct or pnl_pct >= settings.take_profit_pct
