from fastapi import APIRouter, HTTPException

import MetaTrader5 as mt5
from app.mt5 import orders

router = APIRouter()

@router.get("/")
def get_open_orders():
    return orders.get_open_orders()

@router.get("/symbol/{symbol}")
def get_open_orders_by_symbol(symbol: str):
    return orders.get_open_orders_from_symbol(symbol)

@router.get("/group/{group}")
def get_open_orders_by_symbol(group: str):
    return orders.get_open_orders_by_group(group)

@router.get("/ticket/{ticket}")
def get_open_order_by_ticket(ticket: int):
    return orders.get_open_order_by_ticket(ticket)

@router.post("/send/")
def send_order(symbol: str, 
                 order_type: int, 
                 volume: float, 
                 sl_points: int = 0, 
                 tp_points: int = 0, 
                 deviation: int = 10, 
                 type_time: int = mt5.ORDER_TIME_GTC, 
                 type_filling: int = mt5.ORDER_FILLING_RETURN, 
                 comment: str = "", 
                 magic: int = 12345):
    return orders.send_request(
        symbol=symbol,
        order_type=order_type,
        volume=volume,
        sl_points=sl_points,
        tp_points=tp_points,
        deviation=deviation,
        type_time=type_time,
        type_filling=type_filling,
        comment=comment,
        magic=magic
    )