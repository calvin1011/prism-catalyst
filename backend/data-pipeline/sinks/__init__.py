"""Sinks consume ingested quotes/OHLCV. Redis for real-time quotes; Postgres for historical OHLCV."""

from .base import QuoteSink, OHLCVSink
from .log_sink import LogSink
from .postgres_sink import PostgresSink
from .redis_sink import RedisSink

__all__ = ["QuoteSink", "OHLCVSink", "LogSink", "RedisSink", "PostgresSink"]
