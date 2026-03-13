from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

from .ai_analyzer import AIAnalyzer
from .config import settings
from .news_client import NewsClient
from .polymarket_client import PolymarketClient
from .strategy import Strategy
from .telegram_notifier import TelegramNotifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def run() -> None:
    poly = PolymarketClient()
    news_client = NewsClient()
    ai = AIAnalyzer()
    strategy = Strategy()
    tg = TelegramNotifier()

    logging.info("Bot started. dry_run=%s", settings.dry_run)
    tg.send(f"Polymarket bot started. dry_run={settings.dry_run}")

    while True:
        try:
            markets = poly.get_markets()
            selected = strategy.pick_markets(markets)
            open_positions = poly.get_open_positions()

            indexed = {m.id: m for m in selected}
            for pos in open_positions:
                m = indexed.get(pos.market_id)
                if not m:
                    continue
                if strategy.should_close(pos, m.yes_price):
                    result = poly.close_position(pos)
                    logging.info("Closed position %s: %s", pos.market_id, result)
                    tg.send(f"Closed position {pos.market_id}: {result}")

            for m in selected:
                articles = news_client.fetch_related_news(m.question)
                signal = ai.analyze_market(m, articles)
                if not signal:
                    continue
                if strategy.should_open(m, signal, open_positions):
                    order = poly.place_order(
                        market_id=m.id,
                        side=signal.side,
                        size_usd=settings.max_position_usd,
                        limit_price=m.yes_price if signal.side == "YES" else m.no_price,
                    )
                    logging.info("Open %s %s: %s", m.id, signal.side, order)
                    tg.send(
                        f"Open {m.id} {signal.side}, fair_yes={signal.fair_prob_yes:.2f}, "
                        f"conf={signal.confidence:.2f}, reason={signal.reason}"
                    )

            time.sleep(settings.scan_interval_sec)
        except Exception as exc:
            logging.exception("Main loop failed: %s", exc)
            tg.send(f"Bot error at {datetime.now(timezone.utc).isoformat()}: {exc}")
            time.sleep(15)


if __name__ == "__main__":
    run()
