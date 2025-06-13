from fastapi import APIRouter, HTTPException
from app.mt5 import account

router = APIRouter()

@router.get("/")
def account_info():
    info = account.get_account_info()
    if not info:
        raise HTTPException(status_code=500, detail="Account info not available")
    return info

@router.get("/portfolio/stats")
def portfolio():
    return account.get_portfolio_stats()