from fastapi import APIRouter
from pydantic import BaseModel, Field
from services.trade_service import TradeService

router = APIRouter()
trade_service = TradeService()

# === Shared Base Schema ===

class TradeRequest(BaseModel):
    """Market order request schema."""
    symbol: str = Field(..., example="EURUSD")
    volume: float = Field(..., gt=0, example=0.1)
    sl: float | None = Field(None, description="Stop Loss")
    tp: float | None = Field(None, description="Take Profit")
    deviation: int = Field(10, description="Max price deviation")
    magic: int = Field(0, description="Magic number for identification")

class PendingOrderRequest(TradeRequest):
    """Pending order request schema (includes price)."""
    price: float = Field(..., gt=0, description="Pending order price")

class ModifyOrderRequest(BaseModel):
    """Schema to modify an existing pending order."""
    order_id: int = Field(..., description="Order ticket to modify")
    new_price: float = Field(..., gt=0)
    new_sl: float | None = Field(None)
    new_tp: float | None = Field(None)

class ClosePositionRequest(BaseModel):
    """Schema to close an open position."""
    ticket: int = Field(..., description="Ticket ID of the position")

# === Market Orders ===

@router.post("/trade/buy", summary="Execute Buy Market Order")
def buy(req: TradeRequest):
    return trade_service.buy(**req.dict())

@router.post("/trade/sell", summary="Execute Sell Market Order")
def sell(req: TradeRequest):
    return trade_service.sell(**req.dict())

# === Pending Orders ===

@router.post("/trade/buy_limit", summary="Place Buy Limit Order")
def buy_limit(req: PendingOrderRequest):
    return trade_service.buy_limit(**req.dict())

@router.post("/trade/sell_limit", summary="Place Sell Limit Order")
def sell_limit(req: PendingOrderRequest):
    return trade_service.sell_limit(**req.dict())

@router.post("/trade/buy_stop", summary="Place Buy Stop Order")
def buy_stop(req: PendingOrderRequest):
    return trade_service.buy_stop(**req.dict())

@router.post("/trade/sell_stop", summary="Place Sell Stop Order")
def sell_stop(req: PendingOrderRequest):
    return trade_service.sell_stop(**req.dict())

# === Position & Order Actions ===

@router.post("/trade/close", summary="Close Position by Ticket")
def close_position(req: ClosePositionRequest):
    return trade_service.close_position(ticket=req.ticket)

@router.post("/trade/modify", summary="Modify Pending Order")
def modify_order(req: ModifyOrderRequest):
    return trade_service.modify_order(
        order_id=req.order_id,
        new_price=req.new_price,
        new_sl=req.new_sl,
        new_tp=req.new_tp
    )
