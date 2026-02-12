"""Ingestion job: fetch quotes (and optionally daily OHLCV) for a symbol list and write to sinks."""

import logging
import time
from typing import Sequence

from config import INGEST_QUOTE_DELAY_SECONDS
from models import OHLCV, Quote
from providers import AlphaVantageClient
from sinks import LogSink, OHLCVSink, QuoteSink

logger = logging.getLogger(__name__)


def run_ingestion(
    symbols: Sequence[str],
    quote_sinks: Sequence[QuoteSink],
    ohlcv_sinks: Sequence[OHLCVSink],
    *,
    fetch_daily: bool = False,
    delay_seconds: float = INGEST_QUOTE_DELAY_SECONDS,
    client: AlphaVantageClient | None = None,
) -> None:
    if not symbols:
        logger.warning("no symbols to ingest")
        return
    av = client or AlphaVantageClient()
    for i, symbol in enumerate(symbols):
        try:
            quote = av.get_quote(symbol)
            for s in quote_sinks:
                s.write_quote(quote)
            if fetch_daily:
                series = av.get_daily_series(symbol, outputsize="compact")
                for s in ohlcv_sinks:
                    s.write_ohlcv_batch(symbol, series)
        except Exception as e:
            logger.exception("ingest %s: %s", symbol, e)
        if i < len(symbols) - 1 and delay_seconds > 0:
            time.sleep(delay_seconds)
