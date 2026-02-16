"""Sinks consume ingested quotes/OHLCV. Redis for real-time quotes; DB in later Phase 2."""

from .base import QuoteSink, OHLCVSink
from .log_sink import LogSink
from .redis_sink import RedisSink

__all__ = ["QuoteSink", "OHLCVSink", "LogSink", "RedisSink"]
