from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import app.mt5.ticks as ticks

router = APIRouter()

@router.get("/from/")
def get_ticks_from(
    symbol: str,
    from_datetime: datetime = Query(..., description="Start time in ISO format (e.g. 2024-01-01T00:00:00)"),
    count: int = Query(50, description="Number of ticks to fetch"),
    flags: int = Query(1, description="Tick type flag: 1 = all, 2 = trade, 4 = bid, 8 = ask")
):
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

@router.get("/range/")
def get_ticks_range(
    symbol: str,
    from_datetime: datetime = Query(..., description="Start time in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End time in ISO format (e.g. 2024-01-01T00:00:00)"),
    flags: int = Query(1, description="Tick type flag: 1 = all, 2 = trade, 4 = bid, 8 = ask")
):
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