from fastapi import APIRouter, HTTPException
from app.mt5 import positions

router = APIRouter()

@router.get(
    "/",
    summary="Get all open positions",
    response_description="List of currently active/open positions"
)
def open_positions():
    """
    Retrieve all currently open (active) trading positions from the MetaTrader 5 terminal.

    Returns:
        JSON object containing:
        - `success`: Whether the query was successful.
        - `position_count`: Number of open positions.
        - `positions`: List of open position objects.

    Raises:
        HTTPException: If retrieval fails or no data is returned.
    """
    result = positions.get_open_positions()

    if result is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve open positions")

    return {
        "success": True,
        "position_count": len(result),
        "positions": result
    }

@router.get(
    "/symbol/{symbol}",
    summary="Get open positions by symbol",
    response_description="List of open trading positions for a given symbol"
)
def get_open_positions_by_symbol(symbol: str):
    """
    Retrieve all currently open (active) positions for a specific trading symbol.

    Args:
        symbol (str): Trading symbol to filter positions (e.g., 'EURUSD', 'BTCUSD').

    Returns:
        JSON object containing:
        - `success`: Whether the query was successful.
        - `symbol`: The queried trading symbol.
        - `position_count`: Number of open positions for the symbol.
        - `positions`: List of matching position objects.

    Raises:
        HTTPException: If no positions are found or the request fails.
    """
    positions_list = positions.get_open_positions_from_symbol(symbol)

    if positions_list is None:
        raise HTTPException(status_code=404, detail=f"No open positions found for symbol '{symbol}'")

    return {
        "success": True,
        "symbol": symbol,
        "position_count": len(positions_list),
        "positions": positions_list
    }

@router.get(
    "/group/{group}",
    summary="Get open positions by symbol group",
    response_description="List of open positions filtered by a symbol group"
)
def get_open_positions_by_symbol(group: str):
    """
    Retrieve all open (active) trading positions for symbols matching a given group pattern.

    Args:
        group (str): A symbol group filter (e.g., 'USD*', '*BTC*', or 'Retail\\Forex\\Major\\*').

    Returns:
        JSON object containing:
        - `success`: Whether the query was successful.
        - `group`: The group pattern used for filtering.
        - `position_count`: Number of positions found.
        - `positions`: List of matching position objects.

    Raises:
        HTTPException: If no positions are found or MT5 query fails.
    """
    positions_list = positions.get_open_positions_by_group(group)

    if positions_list is None:
        raise HTTPException(status_code=404, detail=f"No open positions found for group '{group}'")

    return {
        "success": True,
        "group": group,
        "position_count": len(positions_list),
        "positions": positions_list
    }

@router.get(
    "/ticket/{ticket}",
    summary="Get open position by ticket",
    response_description="Retrieve a single open position using its ticket number"
)
def get_open_position_by_ticket(ticket: int):
    """
    Retrieve a specific open trading position by its unique ticket ID.

    Args:
        ticket (int): The position's ticket number.

    Returns:
        JSON object containing:
        - `success`: Whether the query was successful.
        - `ticket`: The queried ticket ID.
        - `position`: The matching position details.

    Raises:
        HTTPException: If the position is not found or the MT5 query fails.
    """
    position = positions.get_open_position_by_ticket(ticket)

    if position is None:
        raise HTTPException(status_code=404, detail=f"No open position found for ticket '{ticket}'")

    return {
        "success": True,
        "ticket": ticket,
        "position": position
    }
