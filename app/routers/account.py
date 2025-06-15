from fastapi import APIRouter, HTTPException
from app.mt5 import account

router = APIRouter()

@router.get("/", summary="Get account details", 
    response_description="Current trading account information")
def account_info():
    """
    Fetches the current account's trading information from MetaTrader 5.

    This includes:
    - Balance
    - Equity
    - Margin usage
    - Account leverage
    - Currency
    - Server name, etc.

    Returns:
        A dictionary with the account info fields, or raises an error if unavailable.
    """

    info = account.get_account_info()
    if not info:
        raise HTTPException(status_code=500, detail="Account info not available")
    return info

@router.get("/portfolio/stats", summary="Get portfolio performance metrics", 
    response_description="Basic account portfolio performance overview")
def portfolio():
    """
    Calculates and returns basic statistics on the current account's portfolio.

    This may include:
    - Net profit/loss
    - Number of open positions
    - Total volume
    - Win/loss ratio
    - Average trade duration

    Returns:
        A dictionary of portfolio metrics based on recent trading activity.
    """
    return account.get_portfolio_stats()