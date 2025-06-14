from datetime import datetime

import MetaTrader5 as mt5

def get_book(symbol:str):
    if not mt5.market_book_add(symbol):
        return None

    book = mt5.market_book_get(symbol)

    mt5.market_book_release(symbol)

    if book is None:
        return None

    return book