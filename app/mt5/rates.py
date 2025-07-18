from datetime import datetime
from typing import Optional

import MetaTrader5 as mt5

# === Timeframe Mapping ===
TIMEFRAME_MAP = {
    1: mt5.TIMEFRAME_M1,
    5: mt5.TIMEFRAME_M5,
    15: mt5.TIMEFRAME_M15,
    30: mt5.TIMEFRAME_M30,
    60: mt5.TIMEFRAME_H1,
    240: mt5.TIMEFRAME_H4,
    1440: mt5.TIMEFRAME_D1,
    10080: mt5.TIMEFRAME_W1,
    43200: mt5.TIMEFRAME_MN1,
}


def get_rates(symbol: str, timeframe: int, from_datetime: datetime, count: int) -> Optional[list[dict]]:
    """
    Fetch historical rates (OHLCV) for a given symbol starting from a datetime.

    Args:
        symbol (str): Trading symbol (e.g., "EURUSD")
        timeframe (int): Minutes (1, 5, 15, 30, 60, etc.)
        from_datetime (datetime): Start time
        count (int): Number of bars to fetch

    Returns:
        list[dict] or None: List of OHLCV bars or None on failure
    """
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_from(symbol, tf, from_datetime, count)
    if not rates:
        return None

    return [_parse_rate(r) for r in rates]


def get_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int) -> Optional[list[dict]]:
    """
    Fetch historical rates from a specific position index.

    Args:
        symbol (str): Trading symbol
        timeframe (int): Timeframe in minutes
        start_pos (int): Position index
        count (int): Number of bars to fetch

    Returns:
        list[dict] or None
    """
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, tf, start_pos, count)
    if not rates:
        return None

    return [_parse_rate(r) for r in rates]


def get_rates_range(symbol: str, timeframe: int, from_datetime: datetime, to_datetime: datetime) -> Optional[list[dict]]:
    """
    Fetch historical rates between two datetime points.

    Args:
        symbol (str): Trading symbol
        timeframe (int): Timeframe in minutes
        from_datetime (datetime): Start time
        to_datetime (datetime): End time

    Returns:
        list[dict] or None
    """
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_range(symbol, tf, from_datetime, to_datetime)
    if not rates:
        return None

    return [_parse_rate(r) for r in rates]


# === Internal Helper ===

def _parse_rate(rate) -> dict:
    """
    Convert a MetaTrader5 OHLCV record (numpy.void) into a dictionary.

    Returns:
        dict: {'time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'}
    """
    return {
        "time": int(rate['time']),  # Unix timestamp
        "open": float(rate['open']),
        "high": float(rate['high']),
        "low": float(rate['low']),
        "close": float(rate['close']),
        "tick_volume": int(rate['tick_volume']),
        "spread": int(rate['spread']),
        "real_volume": int(rate['real_volume']),
    }
