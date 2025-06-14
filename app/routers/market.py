from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

import app.mt5.market as market


router = APIRouter()

@router.post("/book/{symbol}/get")
def get_market_book(symbol: str):
    book = market.get_book(symbol)

    if book is None:
        return JSONResponse(status_code=404, content={"success": False, "message": f"No market book data for {symbol}"})

    book_data = [entry._asdict() for entry in book]
    return JSONResponse(content={"success": True, "symbol": symbol, "book": book_data})

@router.get("/book/{symbol}/preview")
def preview_book(symbol: str):
    book = market.get_book(symbol)

    if book is None:
        raise HTTPException(status_code=404, detail="No market book data")

    return [entry._asdict() for entry in book]
