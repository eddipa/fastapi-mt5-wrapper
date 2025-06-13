from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
import app.mt5.market as market

router = APIRouter()

@router.get("/symbols")
def all_symbols():
    data = market.get_all_symbols()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch symbols")
    return data

@router.get("/symbols/{symbol}")
def symbol_info(symbol: str):
    data = market.get_symbol_info(symbol)
    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    return data

@router.get("/price/{symbol}")
def tick_info(symbol: str):
    tick = market.get_tick(symbol)
    if not tick:
        raise HTTPException(status_code=404, detail=f"No tick data for {symbol}")
    return tick

@router.post("/symbols/select")
def select(symbol: str):
    if not market.select_symbol(symbol):
        raise HTTPException(status_code=500, detail=f"Failed to select {symbol}")
    return {"message": f"Symbol {symbol} selected"}
