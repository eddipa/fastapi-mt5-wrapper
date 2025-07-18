from fastapi import APIRouter
from pydantic import BaseModel
from services.trade_service import TradeService

router = APIRouter()
trade_service = TradeService()

class TradeRequest(BaseModel):
    symbol: str
    volume: float
    sl: float | None = None
    tp: float | None = None
    deviation: int = 10
    magic: int = 0

@router.post("/trade/buy")
def buy(req: TradeRequest):
    return trade_service.buy(**req.dict())

@router.post("/trade/sell")
def sell(req: TradeRequest):
    return trade_service.sell(**req.dict())