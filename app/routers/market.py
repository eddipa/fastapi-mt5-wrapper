from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

import app.mt5.market as market


router = APIRouter()

@router.post(
    "/book/{symbol}/get",
    summary="Get market book (Level II) data",
    response_description="Market depth (order book) for a given symbol"
)
def get_market_book(symbol: str):
    """
    Retrieve the current market book (Level II depth of market) data for a given trading symbol.

    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSD', 'EURUSD').

    Returns:
        JSON object with:
        - `success`: Boolean indicating result.
        - `symbol`: The queried symbol.
        - `book`: A list of book entries (bids and asks with price and volume).

    Raises:
        404 Error: If no market book is available for the given symbol.
    """
    book = market.get_book(symbol)

    if book is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": f"No market book data for {symbol}"
            }
        )

    book_data = [entry._asdict() for entry in book]
    return JSONResponse(
        content={
            "success": True,
            "symbol": symbol,
            "book": book_data
        }
    )

@router.get(
    "/book/{symbol}/preview",
    summary="Preview market book for a symbol",
    response_description="Raw market book (Level II) data as a list of entries"
)
def preview_book(symbol: str):
    """
    Return a raw list of market book (Level II depth) entries for a given trading symbol.

    Args:
        symbol (str): Trading symbol (e.g., 'EURUSD', 'BTCUSD').

    Returns:
        List of book entries as dictionaries, each representing a bid or ask.

    Raises:
        HTTPException: If no market book data is available for the symbol.
    """
    book = market.get_book(symbol)

    if book is None:
        raise HTTPException(status_code=404, 
                    detail="No market book data available for this symbol.")

    return [entry._asdict() for entry in book]
