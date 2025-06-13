import MetaTrader5 as mt5


def get_open_orders():
    positions = mt5.orders_total() or []
    return {
        "open_orders_count": len(positions),
    }