import MetaTrader5 as mt5
from datetime import datetime
from typing import Optional

# === TICK FLAG MAP ===
TICK_FLAG_MAP = {
    1: mt5.COPY_TICKS_ALL,    # Bid + Ask + Last
    2: mt5.COPY_TICKS_TRADE,  # Last (Trade ticks)
    4: mt5.COPY_TICKS_INFO,   # Bid-only (Info tick)
    8: mt5.COPY_TICKS_INFO,   # Ask-only (same as above)
}


def get_ticks_from(symbol: str, from_datetime: datetime, count: int, flags: int) -> Optional[list[dict]]:
    """
    Get tick data starting from a datetime.

    Args:
        symbol (str): Trading symbol
        from_datetime (datetime): Starting point
        count (int): Number of ticks
        flags (int): Tick type (1 = all, 2 = trade, 4 = bid, 8 = ask)

    Returns:
        list[dict] or None: Tick data or None if empty
    """
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)

    tick_flag = TICK_FLAG_MAP.get(flags)
    if tick_flag is None:
        print(f"Invalid flag: {flags}")
        return None

    ticks = mt5.copy_ticks_from(symbol, from_datetime, count, tick_flag)
    if not ticks:
        return None

    return [_parse_tick(tick) for tick in ticks]


def get_ticks_range(symbol: str, from_datetime: datetime, to_datetime: datetime, flags: int) -> Optional[list[dict]]:
    """
    Get tick data between two datetime points.

    Args:
        symbol (str): Trading symbol
        from_datetime (datetime): Start time
        to_datetime (datetime): End time
        flags (int): Tick type (1 = all, 2 = trade, 4 = bid, 8 = ask)

    Returns:
        list[dict] or None
    """
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)

    tick_flag = TICK_FLAG_MAP.get(flags)
    if tick_flag is None:
        print(f"Invalid flag: {flags}")
        return None

    ticks = mt5.copy_ticks_range(symbol, from_datetime, to_datetime, tick_flag)
    if not ticks:
        return None

    return [_parse_tick(tick) for tick in ticks]


# === Helper ===

def _parse_tick(tick) -> dict:
    """
    Convert tick data (numpy.void) to a serializable dictionary.

    Returns:
        dict: {'time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'}
    """
    return {
        "time": int(tick['time']),
        "bid": float(tick['bid']),
        "ask": float(tick['ask']),
        "last": float(tick['last']),
        "volume": float(tick['volume']),
        "time_msc": int(tick['time_msc']),
        "flags": int(tick['flags']),
        "volume_real": float(tick['volume_real']),
    }
