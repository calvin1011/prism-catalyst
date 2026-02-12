# Data pipeline & market data (Phase 2)

Python service in `backend/data-pipeline/` for ingesting market data. Phase 2 adds one provider (Alpha Vantage); Redis and historical storage come in later deliverables.

## Prerequisites

- Python 3.10+
- Repo root `.env` with `ALPHA_VANTAGE_API_KEY` (get a free key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key); free tier: 25 requests/day).

## Setup

From repo root (so `.env` is loaded):

```bash
cd backend/data-pipeline
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

## Testing the integration

From `backend/data-pipeline` (with `.env` in repo root containing `ALPHA_VANTAGE_API_KEY`):

**Single quote (latest price):**
```bash
python fetch_quote.py AAPL
```

**Daily OHLCV (last 100 days):**
```bash
python fetch_quote.py AAPL --daily
```

Output is JSON to stdout. If the key is missing or invalid, the script exits with an error message.

## Ingestion pipeline

The pipeline fetches quotes (and optionally daily OHLCV) for a list of symbols and writes to **sinks**. Until Redis and PostgreSQL are wired in, the default sink is logging only.

From `backend/data-pipeline`:

```bash
# Quotes only; symbols from INGEST_SYMBOLS (default: AAPL,MSFT,GOOGL) or pass as args
python run_ingestion.py

# Also fetch daily OHLCV per symbol (uses 2 API calls per symbol)
python run_ingestion.py --daily

# Override symbols
python run_ingestion.py AAPL MSFT
```

Optional env (repo root `.env`): `INGEST_SYMBOLS` (comma-separated), `INGEST_QUOTE_DELAY_SECONDS` (delay between API calls; default 12 for free tier).

## Layout

- `config.py` – env: `ALPHA_VANTAGE_API_KEY`, `INGEST_SYMBOLS`, `INGEST_QUOTE_DELAY_SECONDS`
- `models.py` – normalized `Quote` and `OHLCV` (Pydantic) for any provider
- `providers/alpha_vantage.py` – Alpha Vantage client (quote + daily series)
- `sinks/` – `QuoteSink` and `OHLCVSink`; `LogSink` now; Redis/DB sinks in later Phase 2 steps
- `ingest.py` – job runner (fetch → sinks)
- `fetch_quote.py` – CLI to test the API; `run_ingestion.py` – run ingestion job

Additional providers (e.g. Yahoo Finance, IEX) can be added in `providers/` and return the same `Quote`/`OHLCV` models.
