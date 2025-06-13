from fastapi import APIRouter, HTTPException
from app.mt5 import positions

router = APIRouter()

@router.get("/")
def open_positions():
    return positions.get_open_positions()

@router.get("/symbol/{symbol}")
def get_open_positions_by_symbol(symbol: str):
    return positions.get_open_positions_from_symbol(symbol)

@router.get("/group/{group}")
def get_open_positions_by_symbol(group: str):
    return positions.get_open_positions_by_group(group)

@router.get("/ticket/{ticket}")
def get_open_position_by_ticket(ticket: int):
    return positions.get_open_position_by_ticket(ticket)