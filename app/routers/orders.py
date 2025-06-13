from fastapi import APIRouter, HTTPException
from app.mt5 import orders

router = APIRouter()

@router.get("/")
def get_open_orders():
    return orders.get_open_orders()