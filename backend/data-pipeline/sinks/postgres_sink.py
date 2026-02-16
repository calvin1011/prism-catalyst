"""PostgreSQL sink: persist daily OHLCV to price_bars for charts and backtesting."""

import logging

import psycopg2
from psycopg2.extras import execute_values

from models import OHLCV

logger = logging.getLogger(__name__)


class PostgresSink:
    def __init__(self, database_url: str):
        self._url = database_url
        self._conn = None

    def _connect(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(self._url)
        return self._conn

    def write_ohlcv_batch(self, symbol: str, rows: list[OHLCV]) -> None:
        if not rows:
            return
        try:
            conn = self._connect()
            data = [
                (
                    symbol,
                    row.date,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume,
                    row.source or "alpha_vantage",
                )
                for row in rows
            ]
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO price_bars (symbol, bar_date, open, high, low, close, volume, source)
                    VALUES %s
                    ON CONFLICT (symbol, bar_date) DO UPDATE SET
                      open = EXCLUDED.open,
                      high = EXCLUDED.high,
                      low = EXCLUDED.low,
                      close = EXCLUDED.close,
                      volume = EXCLUDED.volume,
                      source = EXCLUDED.source
                    """,
                    data,
                    template="(%s, %s, %s, %s, %s, %s, %s, %s)",
                )
            conn.commit()
            logger.info("postgres price_bars %s rows=%d", symbol, len(rows))
        except Exception as e:
            logger.exception("postgres write_ohlcv_batch %s: %s", symbol, e)
            if self._conn and not self._conn.closed:
                try:
                    self._conn.rollback()
                except Exception:
                    pass

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
