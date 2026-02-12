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
