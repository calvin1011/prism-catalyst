"""Fetch a single quote from Alpha Vantage. Run from backend/data-pipeline with .env set.

Usage:
  python fetch_quote.py AAPL
  python fetch_quote.py IBM --daily
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import ALPHA_VANTAGE_API_KEY
from providers import AlphaVantageClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch market data via Alpha Vantage")
    parser.add_argument("symbol", help="Ticker symbol (e.g. AAPL)")
    parser.add_argument("--daily", action="store_true", help="Fetch daily OHLCV series (compact)")
    args = parser.parse_args()

    if not ALPHA_VANTAGE_API_KEY:
        print("Error: ALPHA_VANTAGE_API_KEY not set. Add it to .env in the repo root.", file=sys.stderr)
        sys.exit(1)

    client = AlphaVantageClient()
    try:
        if args.daily:
            series = client.get_daily_series(args.symbol, outputsize="compact")
            print(json.dumps([p.model_dump(mode="json") for p in series], indent=2))
        else:
            quote = client.get_quote(args.symbol)
            print(quote.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
