"""Load config from environment. No secrets in repo; use .env or env vars."""

import os
from pathlib import Path

from dotenv import load_dotenv

_env_dir = Path(__file__).resolve().parent
_root = _env_dir.parent.parent
load_dotenv(_root / ".env")
load_dotenv(_env_dir / ".env")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def _symbols() -> list[str]:
    raw = os.getenv("INGEST_SYMBOLS", "AAPL,MSFT,GOOGL").strip()
    return [s.strip().upper() for s in raw.split(",") if s.strip()]

INGEST_SYMBOLS = _symbols()
INGEST_QUOTE_DELAY_SECONDS = float(os.getenv("INGEST_QUOTE_DELAY_SECONDS", "12"))

REDIS_URL = os.getenv("REDIS_URL", "").strip()
QUOTE_CACHE_TTL_SECONDS = int(os.getenv("QUOTE_CACHE_TTL_SECONDS", "300"))

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
