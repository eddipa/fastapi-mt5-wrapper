from fastapi import APIRouter, HTTPException

from app.mt5 import terminal

router = APIRouter()

@router.get("/info/")
def get_terminal():
    return terminal.get_terminal_info()