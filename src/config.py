from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    polymarket_api_base: str = "https://clob.polymarket.com"
    polymarket_api_key: str = ""
    polymarket_api_secret: str = ""
    polymarket_private_key: str = ""

    openai_api_base: str = "https://api.openai.com/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    news_api_base: str = "https://newsapi.org/v2"
    news_api_key: str = ""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    scan_interval_sec: int = 60
    min_liquidity: float = 5000
    max_spread_bps: float = 300
    min_edge_to_open: float = 0.06

    max_position_usd: float = 25
    max_open_positions: int = 5
    stop_loss_pct: float = 0.25
    take_profit_pct: float = 0.30
    max_position_lifetime_min: int = 360

    dry_run: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
