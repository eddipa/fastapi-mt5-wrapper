import MetaTrader5 as mt5

from datetime import datetime


TICK_FLAG_MAP = {
    1: mt5.COPY_TICKS_ALL,    # All ticks (bid + ask + last)
    2: mt5.COPY_TICKS_TRADE,  # Trade ticks only (last)
    4: mt5.COPY_TICKS_INFO,   # Bid-only ticks
    8: mt5.COPY_TICKS_INFO,   # Ask-only ticks (use with caution, usually combined)
}

def get_ticks_from(symbol: str, from_datetime: datetime, count: int, flags: int):
    if not mt5.initialize():
        return None

    tick_flag = TICK_FLAG_MAP.get(flags)
    if tick_flag is None:
        print(f"Invalid flag: {flags}")
        return None

    ticks = mt5.copy_ticks_from(symbol, from_datetime, count, tick_flag)

    if ticks is None or len(ticks) == 0:
        return None

    tick_list = []
    for tick in ticks:
        tick_list.append({
            "time": int(tick['time']),
            "bid": float(tick['bid']),
            "ask": float(tick['ask']),
            "last": float(tick['last']),
            "volume": float(tick['volume']),
            "time_msc": int(tick['time_msc']),
            "flags": int(tick['flags']),
            "volume_real": float(tick['volume_real']),
        })

    return tick_list

def get_ticks_range(symbol: str, from_datetime: datetime, to_datetime: datetime, flags: int):
    if not mt5.initialize():
        return None
        
    tick_flag = TICK_FLAG_MAP.get(flags)
    if tick_flag is None:
        print(f"Invalid flag: {flags}")
        return None

    ticks = mt5.copy_ticks_range(symbol, from_datetime, to_datetime, tick_flag)

    if ticks is None or len(ticks) == 0:
        return None

    tick_list = []
    for tick in ticks:
        tick_list.append({
            "time": int(tick['time']),
            "bid": float(tick['bid']),
            "ask": float(tick['ask']),
            "last": float(tick['last']),
            "volume": float(tick['volume']),
            "time_msc": int(tick['time_msc']),
            "flags": int(tick['flags']),
            "volume_real": float(tick['volume_real']),
        })