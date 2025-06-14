from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import MetaTrader5 as mt5
from app.mt5 import orders

router = APIRouter()

class MarginRequest(BaseModel):
    action: int
    symbol: str
    volume: float
    price: Optional[float] = None

class ProfitRequest(BaseModel):
    action: int
    symbol: str
    volume: float
    price_open: float
    price_close: float

class OrderCheckRequest(BaseModel):
    request: Dict[str, Any]

class OrderSendRequest(BaseModel):
    request: Dict[str, Any]

@router.get("/")
def get_open_orders():
    return orders.get_orders()

@router.get("/symbol/{symbol}")
def get_open_orders_by_symbol(symbol: str):
    return orders.get_open_orders_from_symbol(symbol)

@router.get("/group/{group}")
def get_open_orders_by_symbol(group: str):
    return orders.get_open_orders_by_group(group)

@router.get("/ticket/{ticket}")
def get_open_order_by_ticket(ticket: int):
    return orders.get_open_order_by_ticket(ticket)

@router.post("/calc-margin/")
def calculate_margin(req: MarginRequest):
    margin, error = orders.calc_margin(req.action, req.symbol, req.volume, req.price)

    if margin is None:
        raise HTTPException(status_code=400, detail=error or "Failed to calculate margin")

    return {
        "success": True,
        "symbol": req.symbol,
        "volume": req.volume,
        "price_used": req.price if req.price else "auto",
        "margin": margin
    }

@router.post("/calc-profit/")
def calculate_profit(req: ProfitRequest):
    profit, error = orders.calc_profit(req.action, req.symbol, req.volume, req.price_open, req.price_close)

    if profit is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "symbol": req.symbol,
        "volume": req.volume,
        "price_open": req.price_open,
        "price_close": req.price_close,
        "profit": profit
    }


@router.post("/check/")
def check_order(req: OrderCheckRequest):
    result, error = orders.order_check(req.request)

    if result is None:
        raise HTTPException(status_code=400, detail=error)
    
    result["retcode_message"] = orders.parse_order_retcode(result["retcode"])

    return {
        "success": True,
        "check_result": result
    }

@router.post("/send/")
def send_order(req: OrderSendRequest):
    result, error = orders.order_send(req.request)

    if result is None:
        raise HTTPException(status_code=400, detail=error)

    result["retcode_message"] = orders.parse_order_retcode(result["retcode"])

    return {
        "success": True,
        "send_result": result
    }