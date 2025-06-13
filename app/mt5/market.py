from datetime import datetime
from enum import Enum

from fastapi import Query
import MetaTrader5 as mt5


def get_all_symbols():
    symbols = mt5.symbols_get()
    return [s._asdict() for s in symbols] if symbols else None

def get_symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    return info._asdict() if info else None

def get_tick(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    return tick._asdict() if tick else None

def select_symbol(symbol: str) -> bool:
    return mt5.symbol_select(symbol, True)
