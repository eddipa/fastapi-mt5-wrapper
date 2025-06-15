from datetime import datetime
import MetaTrader5 as mt5

from app.mt5.helpers import (
    map_trade_mode, map_calc_mode, map_filling_type,
    map_exemode, format_timestamp, decode_tick_flags, 
    format_timestamp, 
)

def get_all_symbols():
    symbols = mt5.symbols_get()
    return [s._asdict() for s in symbols] if symbols else None

def get_symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    
    if not info:
        return None

    d = info._asdict()

    # Add prettified values
    d["trade_mode_readable"] = map_trade_mode(d["trade_mode"])
    d["trade_calc_mode_readable"] = map_calc_mode(d["trade_calc_mode"])
    d["filling_mode_readable"] = map_filling_type(d["filling_mode"])
    d["trade_exemode_readable"] = map_exemode(d["trade_exemode"])
    d["start_time_readable"] = format_timestamp(d["start_time"])
    d["expiration_time_readable"] = format_timestamp(d["expiration_time"])
    d["time_readable"] = format_timestamp(d["time"])

    return d

def get_symbol_info_tick(symbol: str):
    info = mt5.symbol_info_tick(symbol)
    
    if not info:
        return None

    d = info._asdict()

    # Add prettified fields
    d["time_readable"] = format_timestamp(d["time"])
    d["flags_readable"] = decode_tick_flags(d["flags"])

    return d

def select_symbol(symbol: str) -> bool:
    symbol_info = get_symbol_info(symbol)
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        sym_select = mt5.symbol_select(symbol,True)
        if not sym_select:
            print("symbol_select({}}) failed, exit",symbol)
            return False

    return sym_select

