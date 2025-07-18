import MetaTrader5 as mt5
from typing import Optional


def get_open_positions():
    """
    Get summary stats of all open positions.

    Returns:
        dict: Total count, volume, and profit of open positions.
    """
    positions = mt5.positions_get() or []
    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
    }


def get_open_positions_from_symbol(symbol: str):
    """
    Get detailed open positions for a given symbol.

    Args:
        symbol (str): Trading symbol (e.g., "EURUSD")

    Returns:
        dict: Summary and position details keyed by index.
    """
    positions = mt5.positions_get(symbol=symbol) or []

    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
        "positions": {i: p._asdict() for i, p in enumerate(positions)}
    }


def get_open_positions_by_group(group: str):
    """
    Get detailed open positions by group.

    Args:
        group (str): Group name or mask (e.g., "EUR*")

    Returns:
        dict: Summary and position details keyed by index.
    """
    positions = mt5.positions_get(group=group) or []

    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
        "positions": {i: p._asdict() for i, p in enumerate(positions)}
    }


def get_open_position_by_ticket(ticket: int):
    """
    Get a single open position by its ticket number.

    Args:
        ticket (int): MT5 position ticket

    Returns:
        dict: Position details or error message
    """
    positions = mt5.positions_get(ticket=ticket) or []
    if positions:
        return positions[0]._asdict()
    return {"error": f"No open position found for ticket {ticket}"}
