from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import app.mt5.rates as rates

router = APIRouter()

@router.get("/")
def get_rates(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe constant like 60 (H1), 5 (M5), etc."),
    from_datetime: datetime = Query(..., description="Start time in ISO format (e.g. 2024-01-01T00:00:00)"),
    count: int = Query(100, description="Number of bars to fetch"),
):
    _rates = rates.get_rates(symbol, timeframe, from_datetime, count)

    if _rates is None:
        raise HTTPException(status_code=404, detail="No rates returned")

    return {"success": True, "symbol": symbol, "timeframe": timeframe, "count": len(_rates), "rates": _rates}

@router.get("/pos/")
def get_rates_from_position(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe as int (e.g. 60 for H1)"),
    start_pos: int = Query(0, description="Start position (offset from the most recent bar)"),
    count: int = Query(100, description="Number of bars to retrieve")
):
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

@router.get("/range/")
def get_rates_range(
    symbol: str,
    timeframe: int = Query(..., description="MT5 timeframe as int (e.g. 60 for H1)"),
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)")
):
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