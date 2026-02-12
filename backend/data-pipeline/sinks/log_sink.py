"""Log sink: writes quotes and OHLCV to stdout/log. Used until Redis and DB sinks exist."""

import logging
from models import OHLCV, Quote

logger = logging.getLogger(__name__)


class LogSink:
    def write_quote(self, quote: Quote) -> None:
        logger.info("quote %s price=%s volume=%s", quote.symbol, quote.price, quote.volume)

    def write_ohlcv_batch(self, symbol: str, rows: list[OHLCV]) -> None:
        logger.info("ohlcv %s count=%d", symbol, len(rows))
