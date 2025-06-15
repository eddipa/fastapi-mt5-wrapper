from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import app.mt5.rates as rates

router = APIRouter()

@router.get(
    "/",
    summary="Get historical rates (bars)",
    response_description="Retrieve historical OHLCV bar data for a given symbol and timeframe"
)
def get_rates(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe constant (e.g. 60 for H1, 5 for M5)"),
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    count: int = Query(100, description="Number of bars to fetch")
):
    """
    Fetch historical bar (candlestick) data for a given symbol and timeframe.

    Args:
        symbol (str): Trading symbol to query (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., 1=M1, 5=M5, 60=H1).
        from_datetime (datetime): Start time for data retrieval.
        count (int): Number of bars to retrieve.

    Returns:
        JSON object containing:
        - `success`: Whether the request succeeded.
        - `symbol`: Queried symbol.
        - `timeframe`: Timeframe in MT5 constant format.
        - `count`: Number of bars returned.
        - `rates`: List of OHLCV bar dictionaries.

    Raises:
        HTTPException: If no rates are returned or the MT5 call fails.
    """
    _rates = rates.get_rates(symbol, timeframe, from_datetime, count)

    if _rates is None:
        raise HTTPException(status_code=404, detail="No rates returned")

    return {
        "success": True,
        "symbol": symbol,
        "timeframe": timeframe,
        "count": len(_rates),
        "rates": _rates
    }

@router.get(
    "/position/",
    summary="Get rates from position offset",
    response_description="Retrieve historical bars starting from a position offset (0 = latest)"
)
def get_rates_from_position(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe as int (e.g. 60 for H1)"),
    start_pos: int = Query(0, description="Start position (0 = most recent bar, 1 = previous, etc.)"),
    count: int = Query(100, description="Number of bars to retrieve")
):
    """
    Fetch historical OHLCV data using a position-based offset from the most recent bar.

    Args:
        symbol (str): The trading symbol (e.g., 'BTCUSD').
        timeframe (int): MT5 timeframe constant.
        start_pos (int): Offset from the latest bar (0 = current, 1 = previous, etc.).
        count (int): Number of bars to fetch from the offset.

    Returns:
        JSON object containing:
        - `success`: Whether data was retrieved successfully.
        - `symbol`: Queried symbol.
        - `timeframe`: MT5 timeframe constant.
        - `start_pos`: Offset used.
        - `count`: Number of bars returned.
        - `rates`: List of OHLCV bar data.

    Raises:
        HTTPException: If data retrieval fails or no data is returned.
    """
    _rates = rates.get_rates_from_pos(symbol, timeframe, start_pos, count)

    if _rates is None:
        raise HTTPException(status_code=404, detail="No rates returned")

    return {
        "success": True,
        "symbol": symbol,
        "timeframe": timeframe,
        "count": len(_rates),
        "start_pos": start_pos,
        "rates": _rates
    }

@router.get(
    "/range/",
    summary="Get historical rates by datetime range",
    response_description="Retrieve OHLCV bars for a symbol within a specific time range"
)
def get_rates_range(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe as int (e.g. 60 for H1)"),
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)")
):
    """
    Retrieve historical OHLCV bar data for a given symbol and timeframe,
    constrained by a specific datetime range.

    Args:
        symbol (str): Trading symbol (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., 5 = M5, 60 = H1).
        from_datetime (datetime): Start time of the range.
        to_datetime (datetime): End time of the range.

    Returns:
        JSON object containing:
        - `success`: Status of the query.
        - `symbol`: Queried symbol.
        - `timeframe`: Timeframe used.
        - `from`: Start time (ISO format).
        - `to`: End time (ISO format).
        - `count`: Number of bars returned.
        - `rates`: List of OHLCV bars in dictionary format.

    Raises:
        HTTPException: If no data is returned.
    """
    _rates = rates.get_rates_range(symbol, timeframe, from_datetime, to_datetime)

    if _rates is None:
        raise HTTPException(status_code=404, detail="No rates returned")

    return {
        "success": True,
        "symbol": symbol,
        "timeframe": timeframe,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "count": len(_rates),
        "rates": _rates
    }
