import MetaTrader5 as mt5


def get_open_positions():
    positions = mt5.positions_get() or []
    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
    }

def get_open_positions_from_symbol(symbol: str):
    positions = mt5.positions_get(symbol=symbol) or []

    positions_dict = {}

    for counter, p in enumerate(positions):
        position = p._asdict()
        positions_dict[counter] = position

    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
        "positions": positions_dict
    }

def get_open_positions_by_group(group: str):
    positions = mt5.positions_get(group=group) or []

    positions_dict = {}

    for counter, p in enumerate(positions):
        position = p._asdict()
        positions_dict[counter] = position

    return {
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
        "positions": positions_dict
    }

def get_open_position_by_ticket(ticket: int):
    positions = mt5.positions_get(ticket=ticket) or []
    if positions:  # not None and not empty
        return positions[0]._asdict()
    else:
        return {"error": f"No open position found for ticket {ticket}"}

