from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import app.mt5.ticks as ticks

router = APIRouter()

@router.get(
    "/from/",
    summary="Get ticks from a start datetime",
    response_description="Retrieve tick data for a symbol starting from a given datetime"
)
def get_ticks_from(
    symbol: str,
    from_datetime: datetime = Query(..., description="Start time in ISO format (e.g. 2024-01-01T00:00:00)"),
    count: int = Query(50, description="Number of ticks to fetch"),
    flags: int = Query(1, description="Tick type flag: 1 = all, 2 = trade, 4 = bid, 8 = ask")
):
    """
    Retrieve raw tick data for a specified symbol beginning at a certain timestamp.

    Args:
        symbol (str): The trading symbol to query (e.g., 'BTCUSD').
        from_datetime (datetime): ISO-format datetime indicating the start time.
        count (int): Number of ticks to fetch.
        flags (int): Bitmask specifying tick types:
                     - 1 = all ticks (default)
                     - 2 = trade ticks only
                     - 4 = bid ticks only
                     - 8 = ask ticks only

    Returns:
        JSON object containing:
        - `success`: Whether the query was successful.
        - `symbol`: Queried symbol.
        - `from`: Start time (ISO format).
        - `count`: Number of ticks returned.
        - `ticks`: List of tick data.

    Raises:
        HTTPException: If no tick data is returned.
    """
    _ticks = ticks.get_ticks_from(symbol, from_datetime, count, flags)

    if _ticks is None:
        raise HTTPException(status_code=404, detail="No tick data returned")

    return {
        "success": True,
        "symbol": symbol,
        "from": from_datetime.isoformat(),
        "count": len(_ticks),
        "ticks": _ticks
    }

@router.get(
    "/range/",
    summary="Get ticks within a time range",
    response_description="Retrieve tick data for a symbol between two datetime boundaries"
)
def get_ticks_range(
    symbol: str,
    from_datetime: datetime = Query(..., description="Start time in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End time in ISO format (e.g. 2024-01-01T00:00:00)"),
    flags: int = Query(1, description="Tick type flag: 1 = all, 2 = trade, 4 = bid, 8 = ask")
):
    """
    Retrieve historical tick data for a specified trading symbol between two datetime values.

    Args:
        symbol (str): Trading symbol (e.g., 'BTCUSD').
        from_datetime (datetime): Start of the datetime range (inclusive).
        to_datetime (datetime): End of the datetime range (inclusive).
        flags (int): Bitmask for tick types:
                     - 1 = all (default)
                     - 2 = trade ticks
                     - 4 = bid ticks
                     - 8 = ask ticks

    Returns:
        JSON object with:
        - `success`: Operation success flag.
        - `symbol`: Symbol queried.
        - `from`: ISO format of the start time.
        - `to`: ISO format of the end time.
        - `count`: Number of ticks returned.
        - `ticks`: List of tick data dictionaries.

    Raises:
        HTTPException: If no tick data is found in the given range.
    """
    _ticks = ticks.get_ticks_range(symbol, from_datetime, to_datetime, flags)

    if _ticks is None:
        raise HTTPException(status_code=404, detail="No tick data returned")

    return {
        "success": True,
        "symbol": symbol,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "count": len(_ticks),
        "ticks": _ticks
    }
