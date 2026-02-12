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

Output is JSON to stdout. If the key is missing or invalid, the script exits with an error message. Use from other scripts or the ingestion pipeline once Redis/historical storage are in place.

## Layout

- `config.py` – loads `ALPHA_VANTAGE_API_KEY` from env
- `models.py` – normalized `Quote` and `OHLCV` (Pydantic) for any provider
- `providers/alpha_vantage.py` – Alpha Vantage client (quote + daily series)
- `fetch_quote.py` – CLI to test the API integration

Additional providers (e.g. Yahoo Finance, IEX) can be added in `providers/` and return the same `Quote`/`OHLCV` models.
