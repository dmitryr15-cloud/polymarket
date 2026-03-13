# Polymarket AI Bot (starter)

> ⚠️ **Важливо про безпеку**: ключі, які були надіслані в чаті, вважаються скомпрометованими. Перед запуском обов'язково відкличте їх та створіть нові. Не зберігайте секрети в репозиторії.

Це стартовий приклад бота для Polymarket, який:
- періодично сканує ринки;
- аналізує новини через LLM;
- приймає рішення щодо відкриття/закриття позицій за простими правилами ризику;
- надсилає повідомлення в Telegram.

## Можливості
- Фільтрація ринків за ліквідністю/спредом/дедлайном.
- Сентимент/імовірнісна оцінка подій через AI (OpenAI-compatible API).
- Автоматичне відкриття позицій при edge вище порогу.
- Закриття позицій за stop-loss / take-profit / timeout.
- Dry-run режим для безпечного тестування.

## Структура
- `src/main.py` — цикл бота.
- `src/polymarket_client.py` — клієнт для API (заглушки + REST методи).
- `src/news_client.py` — отримання новин.
- `src/ai_analyzer.py` — AI аналіз новин і події.
- `src/strategy.py` — логіка відкриття/закриття.
- `src/telegram_notifier.py` — оповіщення в Telegram.
- `src/config.py` — налаштування через env.

## Швидкий старт (локально)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# відредагуйте .env
python -m src.main
```

## Розгортання на сервері (Ubuntu 22.04+)

### 1) Підготовка сервера
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
git clone <your_repo_url> polymarket-bot
cd polymarket-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cp .env.example .env
```

### 2) Налаштування `.env`
Заповніть змінні:
- `POLYMARKET_API_KEY`
- `POLYMARKET_API_SECRET`
- `POLYMARKET_PRIVATE_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `OPENAI_API_KEY`

### 3) Перевірка в dry-run
```bash
source .venv/bin/activate
export DRY_RUN=true
python -m src.main
```

### 4) Запуск як systemd сервіс
Створіть `/etc/systemd/system/polymarket-bot.service`:
```ini
[Unit]
Description=Polymarket AI Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/polymarket-bot
EnvironmentFile=/home/ubuntu/polymarket-bot/.env
ExecStart=/home/ubuntu/polymarket-bot/.venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активуйте:
```bash
sudo systemctl daemon-reload
sudo systemctl enable polymarket-bot
sudo systemctl start polymarket-bot
sudo systemctl status polymarket-bot
journalctl -u polymarket-bot -f
```

## Рекомендації з безпеки
- Обов'язково встановіть `DRY_RUN=true` на етапі тестування.
- Обмежте `MAX_POSITION_USD` і `MAX_OPEN_POSITIONS`.
- Додайте allowlist ринків перед продом.
- Ротуйте ключі при найменшій підозрі компрометації.

## Юридичне застереження
Це освітній приклад. Торгівля пов'язана з ризиком втрати коштів. Використовуйте на власний ризик та відповідно до локального законодавства.
