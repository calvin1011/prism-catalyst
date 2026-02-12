"""Normalized market data models for use across providers (Alpha Vantage, future Yahoo/IEX)."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Quote(BaseModel):
    symbol: str
    price: Decimal
    change: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    volume: Optional[int] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    open: Optional[Decimal] = None
    previous_close: Optional[Decimal] = None
    timestamp: Optional[datetime] = None
    source: str = "alpha_vantage"


class OHLCV(BaseModel):
    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    symbol: str = ""
    source: str = "alpha_vantage"
