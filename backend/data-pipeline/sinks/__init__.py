"""Sinks consume ingested quotes/OHLCV. Add Redis and DB sinks in later Phase 2 deliverables."""

from .base import QuoteSink, OHLCVSink
from .log_sink import LogSink

__all__ = ["QuoteSink", "OHLCVSink", "LogSink"]
