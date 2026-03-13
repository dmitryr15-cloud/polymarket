from dataclasses import dataclass
from datetime import datetime


@dataclass
class Market:
    id: str
    question: str
    yes_price: float
    no_price: float
    liquidity_usd: float
    close_time: datetime


@dataclass
class Position:
    market_id: str
    side: str  # YES | NO
    size_usd: float
    entry_price: float
    opened_at: datetime


@dataclass
class Signal:
    market_id: str
    side: str
    confidence: float
    fair_prob_yes: float
    reason: str
