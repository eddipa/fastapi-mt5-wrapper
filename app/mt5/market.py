from typing import Optional
import MetaTrader5 as mt5


def get_book(symbol: str) -> Optional[list]:
    """
    Retrieve the market depth (order book) for a given symbol.

    Args:
        symbol (str): The symbol to retrieve market depth for (e.g., "EURUSD").

    Returns:
        list[dict] | None: A list of book entries (as namedtuples) or None if failed.
    """
    # Subscribe to book
    if not mt5.market_book_add(symbol):
        return None

    try:
        book = mt5.market_book_get(symbol)
        if book is None:
            return None
        return book
    finally:
        # Always release the subscription
        mt5.market_book_release(symbol)
