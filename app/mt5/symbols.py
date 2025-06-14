from datetime import datetime

import MetaTrader5 as mt5

def get_all_symbols():
    symbols = mt5.symbols_get()
    return [s._asdict() for s in symbols] if symbols else None

def get_symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    return info._asdict() if info else None

def get_symbol_info_tick(symbol: str):
    info = mt5.symbol_info_tick(symbol)
    return info._asdict() if info else None

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

