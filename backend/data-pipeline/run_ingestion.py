"""Run the ingestion job. Use from backend/data-pipeline with .env in repo root.

Usage:
  python run_ingestion.py              # quotes only, symbols from INGEST_SYMBOLS
  python run_ingestion.py --daily      # quotes + daily OHLCV (uses more API calls)
  python run_ingestion.py AAPL MSFT     # override symbols
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import ALPHA_VANTAGE_API_KEY, INGEST_SYMBOLS, INGEST_QUOTE_DELAY_SECONDS
from ingest import run_ingestion
from sinks import LogSink

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run market data ingestion")
    parser.add_argument("symbols", nargs="*", help="Override symbols (default: INGEST_SYMBOLS)")
    parser.add_argument("--daily", action="store_true", help="Also fetch daily OHLCV per symbol")
    args = parser.parse_args()

    if not ALPHA_VANTAGE_API_KEY:
        print("Error: ALPHA_VANTAGE_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    symbols = [s.upper() for s in args.symbols] if args.symbols else INGEST_SYMBOLS
    if not symbols:
        print("Error: no symbols (set INGEST_SYMBOLS or pass symbols).", file=sys.stderr)
        sys.exit(1)

    log_sink = LogSink()
    run_ingestion(
        symbols,
        quote_sinks=[log_sink],
        ohlcv_sinks=[log_sink],
        fetch_daily=args.daily,
        delay_seconds=INGEST_QUOTE_DELAY_SECONDS,
    )


if __name__ == "__main__":
    main()
