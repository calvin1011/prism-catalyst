"""Redis sink: cache quotes for real-time read by API. Key quote:SYMBOL, JSON value, TTL."""

import json
import logging
from typing import Optional

import redis

from config import QUOTE_CACHE_TTL_SECONDS
from models import OHLCV, Quote

logger = logging.getLogger(__name__)

QUOTE_KEY_PREFIX = "quote:"


def _quote_key(symbol: str) -> str:
    return f"{QUOTE_KEY_PREFIX}{symbol.upper()}"


class RedisSink:
    def __init__(self, redis_url: str, ttl_seconds: int = QUOTE_CACHE_TTL_SECONDS):
        self._client: Optional[redis.Redis] = None
        self._url = redis_url
        self._ttl = ttl_seconds

    def _client_sync(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.from_url(self._url, decode_responses=True)
        return self._client

    def write_quote(self, quote: Quote) -> None:
        try:
            client = self._client_sync()
            key = _quote_key(quote.symbol)
            payload = quote.model_dump(mode="json")
            client.set(key, json.dumps(payload), ex=self._ttl)
        except Exception as e:
            logger.exception("redis write_quote %s: %s", quote.symbol, e)

    def write_ohlcv_batch(self, symbol: str, rows: list[OHLCV]) -> None:
        pass

    def close(self) -> None:
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None
