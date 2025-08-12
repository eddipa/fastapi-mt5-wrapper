from datetime import datetime
import MetaTrader5 as mt5

from app.mt5.helpers import (
    map_trade_mode,
    map_calc_mode,
    map_filling_type,
    map_exemode,
    format_timestamp,
    decode_tick_flags,
)


def get_all_symbols():
    """
    Fetch all available trading symbols from MetaTrader 5.

    Returns:
        list[dict] or None: List of symbol info dictionaries, or None on failure.
    """
    symbols = mt5.symbols_get()
    return [s._asdict() for s in symbols] if symbols else None


def get_symbol_info(symbol: str):
    """
    Retrieve full info for a single trading symbol.

    Args:
        symbol (str): Symbol name (e.g., "EURUSD")

    Returns:
        dict or None: Symbol info with added readable fields.
    """
    info = mt5.symbol_info(symbol)
    if not info:
        return None

    d = info._asdict()

    # Add human-readable fields
    d.update({
        "trade_mode_readable": map_trade_mode(d["trade_mode"]),
        "trade_calc_mode_readable": map_calc_mode(d["trade_calc_mode"]),
        "filling_mode_readable": map_filling_type(d["filling_mode"]),
        "trade_exemode_readable": map_exemode(d["trade_exemode"]),
        "start_time_readable": format_timestamp(d["start_time"]),
        "expiration_time_readable": format_timestamp(d["expiration_time"]),
        "time_readable": format_timestamp(d["time"]),
    })

    return d


def get_symbol_info_tick(symbol: str):
    """
    Get the latest tick data for a given symbol.

    Args:
        symbol (str): Symbol name

    Returns:
        dict or None: Tick data including readable time and flags.
    """
    info = mt5.symbol_info_tick(symbol)
    if not info:
        return None

    d = info._asdict()
    d.update({
        "time_readable": format_timestamp(d["time"]),
        "flags_readable": decode_tick_flags(d["flags"]),
    })

    return d


def select_symbol(symbol: str) -> bool:
    """
    Ensure a symbol is selected (visible) in MarketWatch.

    Args:
        symbol (str): Symbol name

    Returns:
        bool: True if symbol is selected or made visible successfully, else False.
    """
    info = mt5.symbol_info(symbol)
    if not info:
        return False

    if not info.visible:
        print(f"{symbol} is not visible, attempting to enable it...")
        if not mt5.symbol_select(symbol, True):
            print(f"symbol_select({symbol}) failed.")
            return False

    return True
