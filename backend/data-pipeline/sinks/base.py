"""Abstract sinks for ingestion pipeline. Implementations: LogSink now; Redis/DB later."""

from abc import ABC, abstractmethod
from typing import Protocol

from models import OHLCV, Quote


class QuoteSink(Protocol):
    def write_quote(self, quote: Quote) -> None:
        ...


class OHLCVSink(Protocol):
    def write_ohlcv_batch(self, symbol: str, rows: list[OHLCV]) -> None:
        ...
