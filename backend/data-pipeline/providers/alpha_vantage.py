"""Alpha Vantage API client. Free tier: 25 requests/day."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

import requests

from config import ALPHA_VANTAGE_API_KEY, ALPHA_VANTAGE_BASE_URL
from models import OHLCV, Quote


def _decimal(s: Optional[str]) -> Optional[Decimal]:
    if s is None or s == "":
        return None
    try:
        return Decimal(str(s).replace(",", "").strip())
    except Exception:
        return None


def _int(s: Optional[str]) -> Optional[int]:
    if s is None or s == "":
        return None
    try:
        return int(float(str(s).replace(",", "").strip()))
    except Exception:
        return None


def _parse_av_error(payload: dict) -> Optional[str]:
    if "Error Message" in payload:
        return payload["Error Message"]
    if "Note" in payload:
        return payload["Note"]
    return None


class AlphaVantageClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = (api_key or ALPHA_VANTAGE_API_KEY).strip()
        self.base_url = base_url or ALPHA_VANTAGE_BASE_URL
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY is required")

    def _get(self, params: dict[str, str]) -> dict[str, Any]:
        params.setdefault("apikey", self.api_key)
        params.setdefault("datatype", "json")
        r = requests.get(self.base_url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        err = _parse_av_error(data)
        if err:
            raise RuntimeError(f"Alpha Vantage API error: {err}")
        return data

    def get_quote(self, symbol: str) -> Quote:
        """Fetch latest quote for a symbol. One API call per symbol."""
        data = self._get({"function": "GLOBAL_QUOTE", "symbol": symbol.upper()})
        gq = data.get("Global Quote") or {}
        change_pct = gq.get("10. change percent")
        if isinstance(change_pct, str) and change_pct.endswith("%"):
            change_pct = change_pct.rstrip("%").strip()
        return Quote(
            symbol=(gq.get("01. symbol") or symbol).strip(),
            price=_decimal(gq.get("05. price")) or Decimal("0"),
            change=_decimal(gq.get("09. change")),
            change_percent=_decimal(change_pct),
            volume=_int(gq.get("06. volume")),
            high=_decimal(gq.get("03. high")),
            low=_decimal(gq.get("04. low")),
            open=_decimal(gq.get("02. open")),
            previous_close=_decimal(gq.get("08. previous close")),
            timestamp=None,
            source="alpha_vantage",
        )

    def get_daily_series(
        self, symbol: str, outputsize: str = "compact"
    ) -> list[OHLCV]:
        """Fetch daily OHLCV. outputsize: 'compact' (last 100 days) or 'full'."""
        if outputsize not in ("compact", "full"):
            outputsize = "compact"
        data = self._get(
            {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol.upper(),
                "outputsize": outputsize,
            }
        )
        key = "Time Series (Daily)"
        series = data.get(key)
        if not series or not isinstance(series, dict):
            return []
        sym = (data.get("Meta Data", {}).get("2. Symbol") or symbol).strip()
        out: list[OHLCV] = []
        for day_str, ohlcv in series.items():
            try:
                dt = datetime.strptime(day_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            if not isinstance(ohlcv, dict):
                continue
            open_ = _decimal(ohlcv.get("1. open"))
            high = _decimal(ohlcv.get("2. high"))
            low = _decimal(ohlcv.get("3. low"))
            close = _decimal(ohlcv.get("4. close"))
            vol = _int(ohlcv.get("5. volume")) or 0
            if open_ is None and high is None and low is None and close is None:
                continue
            out.append(
                OHLCV(
                    date=dt,
                    open=open_ or Decimal("0"),
                    high=high or Decimal("0"),
                    low=low or Decimal("0"),
                    close=close or Decimal("0"),
                    volume=vol,
                    symbol=sym,
                    source="alpha_vantage",
                )
            )
        out.sort(key=lambda x: x.date)
        return out
