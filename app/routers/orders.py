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

@router.get(
    "/",
    summary="Fetch all open orders",
    response_description="List of currently active/open trade orders"
)
def get_open_orders():
    """
    Retrieve all currently open (active) orders from the MetaTrader 5 terminal.

    Returns:
        JSON list of open orders.

    Raises:
        HTTPException: If no orders are found or if MT5 connection fails.
    """
    open_orders = orders.get_orders()

    if open_orders is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve open orders.")

    return {
        "success": True,
        "order_count": len(open_orders),
        "orders": open_orders
    }

@router.get(
    "/symbol/{symbol}",
    summary="Get open orders by symbol",
    response_description="List of open trade orders for the specified symbol"
)
def get_open_orders_by_symbol(symbol: str):
    """
    Retrieve all currently open (active) orders for a specific trading symbol.

    Args:
        symbol (str): Trading symbol (e.g., 'EURUSD', 'BTCUSD').

    Returns:
        JSON object with:
        - `success`: Whether the query was successful.
        - `symbol`: The queried trading symbol.
        - `order_count`: Number of open orders for the symbol.
        - `orders`: List of open orders for the symbol.

    Raises:
        HTTPException: If the MetaTrader 5 API fails or no orders are returned.
    """
    result = orders.get_open_orders_from_symbol(symbol)

    if result is None:
        raise HTTPException(status_code=404, 
                detail=f"No open orders found for symbol '{symbol}'")

    return {
        "success": True,
        "symbol": symbol,
        "order_count": len(result),
        "orders": result
    }

@router.get(
    "/group/{group}",
    summary="Get open orders by symbol group",
    response_description="List of open trade orders filtered by a symbol group"
)
def get_open_orders_by_symbol(group: str):
    """
    Retrieve all currently open (active) orders for a group of trading symbols.

    Args:
        group (str): A symbol group filter (e.g., 'USD*', '*BTC*', or 'Retail\\Forex\\Major\\*').

    Returns:
        JSON object containing:
        - `success`: Whether the operation was successful.
        - `group`: The symbol group used for filtering.
        - `order_count`: Number of matching open orders.
        - `orders`: List of order objects.

    Raises:
        HTTPException: If no orders are found or if the MetaTrader 5 query fails.
    """
    open_orders = orders.get_open_orders_by_group(group)

    if open_orders is None:
        raise HTTPException(status_code=404, detail=f"No open orders found for group '{group}'")

    return {
        "success": True,
        "group": group,
        "order_count": len(open_orders),
        "orders": open_orders
    }

@router.get(
    "/ticket/{ticket}",
    summary="Get open order by ticket",
    response_description="Fetch a single open order using its ticket number"
)
def get_open_order_by_ticket(ticket: int):
    """
    Retrieve a specific open order using its unique ticket number.

    Args:
        ticket (int): The order's ticket ID.

    Returns:
        JSON object containing the order details, or raises an error if not found.
    """
    order = orders.get_open_order_by_ticket(ticket)

    if order is None:
        raise HTTPException(status_code=404, detail=f"No open order found for ticket '{ticket}'")

    return {
        "success": True,
        "ticket": ticket,
        "order": order
    }


@router.post(
    "/calc-margin/",
    summary="Calculate required margin",
    response_description="Compute the margin required for a specific trade"
)
def calculate_margin(req: MarginRequest):
    """
    Calculate the required margin for a trade based on action, symbol, volume, and price.

    Args:
        req (MarginRequest): Includes action (BUY/SELL), symbol, volume, and optional price.

    Returns:
        JSON object containing:
        - `success`: Whether the calculation succeeded.
        - `symbol`: The trading symbol.
        - `volume`: Requested volume.
        - `price_used`: Price used (manual or auto-fetched).
        - `margin`: Required margin in account currency.
    """
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

@router.post(
    "/calc-profit/",
    summary="Calculate trade profit",
    response_description="Compute the profit from a trade based on open and close prices"
)
def calculate_profit(req: ProfitRequest):
    """
    Calculate the profit of a completed trade given the entry and exit prices.

    Args:
        req (ProfitRequest): Includes action (BUY/SELL), symbol, volume, price_open, and price_close.

    Returns:
        JSON object containing:
        - `success`: Whether the calculation succeeded.
        - `symbol`: The trading symbol.
        - `volume`: Traded volume.
        - `price_open`: Open (entry) price.
        - `price_close`: Close (exit) price.
        - `profit`: Calculated profit in account currency.
    """
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

@router.post(
    "/check/",
    summary="Validate a trading order",
    response_description="Run a pre-check on a trade request without executing it"
)
def check_order(req: OrderCheckRequest):
    """
    Validate a trading order before sending it to the market.

    Args:
        req (OrderCheckRequest): Contains the full order request parameters.

    Returns:
        JSON object containing:
        - `success`: Whether the validation passed.
        - `check_result`: Detailed check response including retcode and interpretation.

    Raises:
        HTTPException: If the order check fails or MT5 returns an error.
    """
    result, error = orders.order_check(req.request)

    if result is None:
        raise HTTPException(status_code=400, detail=error)
    
    result["retcode_message"] = orders.parse_order_retcode(result["retcode"])

    return {
        "success": True,
        "check_result": result
    }

@router.post(
    "/send/",
    summary="Send a trading order",
    response_description="Submit an order to the broker for execution"
)
def send_order(req: OrderSendRequest):
    """
    Send a trade order to the MetaTrader 5 terminal for execution.

    Args:
        req (OrderSendRequest): Contains the complete trading order parameters.

    Returns:
        JSON object containing:
        - `success`: Whether the order was submitted successfully.
        - `send_result`: MT5 response with deal/order ID, price, and retcode message.

    Raises:
        HTTPException: If the order submission fails or MT5 returns an error.
    """
    result, error = orders.order_send(req.request)

    if result is None:
        raise HTTPException(status_code=400, detail=error)

    result["retcode_message"] = orders.parse_order_retcode(result["retcode"])

    return {
        "success": True,
        "send_result": result
    }
