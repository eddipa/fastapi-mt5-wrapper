from datetime import datetime

import MetaTrader5 as mt5

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


def get_rates(symbol: str, timeframe: int, from_datetime: datetime, count: int):
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)
    
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_from(symbol, tf, from_datetime, count)

    if rates is None or len(rates) == 0:
        return None

    # Manually convert numpy.void to dict
    rate_dicts = []
    for rate in rates:
        rate_dicts.append({
            "time": int(rate['time']),  # seconds since epoch
            "open": float(rate['open']),
            "high": float(rate['high']),
            "low": float(rate['low']),
            "close": float(rate['close']),
            "tick_volume": int(rate['tick_volume']),
            "spread": int(rate['spread']),
            "real_volume": int(rate['real_volume']),
        })

    return rate_dicts

def get_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int):
    if not mt5.initialize():
        return None

    mt5.symbol_select(symbol)

    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, 5)

    if rates is None or len(rates) == 0:
        return None

    rate_dicts = []
    for rate in rates:
        rate_dicts.append({
            "time": int(rate['time']),
            "open": float(rate['open']),
            "high": float(rate['high']),
            "low": float(rate['low']),
            "close": float(rate['close']),
            "tick_volume": int(rate['tick_volume']),
            "spread": int(rate['spread']),
            "real_volume": int(rate['real_volume']),
        })

    return rate_dicts

def get_rates_range(symbol: str, timeframe: int, from_datetime: datetime, to_datetime: datetime):
    if not mt5.initialize():
        return None
    
    mt5.symbol_select(symbol)

    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        print(f"Invalid timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_range(symbol, tf, from_datetime, to_datetime)

    if rates is None or len(rates) == 0:
        return None

    rate_dicts = []
    for rate in rates:
        rate_dicts.append({
            "time": int(rate['time']),
            "open": float(rate['open']),
            "high": float(rate['high']),
            "low": float(rate['low']),
            "close": float(rate['close']),
            "tick_volume": int(rate['tick_volume']),
            "spread": int(rate['spread']),
            "real_volume": int(rate['real_volume']),
        })

    return rate_dicts