from fastapi import APIRouter, HTTPException
from app.mt5 import symbols


router = APIRouter()

@router.get("/symbols")
def all_symbols():
    data = symbols.get_all_symbols()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch symbols")
    return data

@router.get("/{symbol}")
def symbol_info(symbol: str):
    data = symbols.get_symbol_info(symbol)
    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    return data

@router.get("/{symbol}/tick")
def symbol_info_tick(symbol: str):
    data = symbols.get_symbol_info_tick(symbol)
    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' or TICK not found")
    return data

@router.post("/{symbol}/select")
def select(symbol: str):
    if not symbols.select_symbol(symbol):
        raise HTTPException(status_code=500, detail=f"Failed to select {symbol}")
    return {"message": f"Symbol {symbol} selected"}
