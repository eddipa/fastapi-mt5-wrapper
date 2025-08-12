from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class OrderSide(str):  # check if enum is better
    BUY = "buy"
    SELL = "sell"


class TimeInForce(str):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class PlaceOrderRequest(BaseModel):
    symbol: str = Field(..., example="EURUSD")
    side: OrderSide = Field(..., example="buy")
    volume: float = Field(..., gt=0, example=0.1)
    price: Optional[float] = Field(None, example=1.08542)
    sl: Optional[float] = Field(None, example=1.08200)
    tp: Optional[float] = Field(None, example=1.09100)
    tif: TimeInForce = Field(default=TimeInForce.GTC)
    comment: Optional[str] = Field(None, example="api-order")
    magic: Optional[int] = Field(None, example=123456)


class PlaceOrderResponse(BaseModel):
    order_id: int = Field(..., example=123456789)
    deal_id: Optional[int] = Field(None, example=987654321)
    symbol: str = Field(..., example="EURUSD")
    side: OrderSide = Field(..., example="buy")
    volume: float = Field(..., example=0.1)
    price: float = Field(..., example=1.08542)
    executed_at: datetime = Field(..., example="2025-08-12T15:21:33Z")


class Position(BaseModel):
    ticket: int = Field(..., example=555001)
    symbol: str = Field(..., example="EURUSD")
    side: OrderSide = Field(..., example="buy")
    volume: float = Field(..., example=0.2)
    price_open: float = Field(..., example=1.08000)
    sl: Optional[float] = Field(None, example=1.07500)
    tp: Optional[float] = Field(None, example=1.09000)
    profit: float = Field(..., example=15.73)
    opened_at: datetime = Field(..., example="2025-08-12T13:00:01Z")
