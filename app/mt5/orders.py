import MetaTrader5 as mt5
from typing import Optional

# === Retcode Translation ===

RET_CODE_MAP = {
    0: "Request executed successfully",
    1: "Request executed partially",
    10004: "Trade server busy",
    10006: "No connection to trade server",
    10007: "Live accounts only",
    10008: "Request timeout",
    10009: "Invalid request",
    10010: "Invalid volume",
    10011: "Invalid price",
    10012: "Invalid stop",
    10013: "Trading disabled",
    10014: "Market closed",
    10015: "Trade timeout",
    10016: "Invalid order",
    10017: "Trade context busy",
    10018: "Expiration denied",
    10019: "Too many requests",
    10020: "Order not found",
    10021: "Unknown symbol",
    10022: "Server busy",
    10023: "Modification failed",
    10024: "Too frequent requests",
    10025: "Order locked",
    10026: "Long-only positions allowed",
    10027: "Too many pending orders",
    10028: "Hedging prohibited",
    10029: "Close-by orders prohibited",
}


def parse_order_retcode(retcode: int) -> str:
    """Convert retcode to human-readable description."""
    return RET_CODE_MAP.get(retcode, f"Unknown retcode ({retcode})")


# === Order Fetching ===

def get_orders():
    """Get total number of open orders."""
    return {"orders_count": mt5.orders_total() or 0}


def get_open_orders_from_symbol(symbol: str):
    """Fetch open orders for a specific symbol."""
    orders = mt5.orders_get(symbol=symbol) or []
    return {
        "open_orders_count": len(orders),
        "open_orders_volume": sum(order.volume for order in orders),
        "orders": {i: o._asdict() for i, o in enumerate(orders)},
    }


def get_open_orders_by_group(group: str):
    """Fetch open orders by symbol group."""
    orders = mt5.orders_get(group=group) or []
    return {
        "open_orders_count": len(orders),
        "open_orders_volume": sum(order.volume for order in orders),
        "orders": {i: o._asdict() for i, o in enumerate(orders)},
    }


def get_open_order_by_ticket(ticket: int):
    """Fetch open order by ticket number."""
    orders = mt5.orders_get(ticket=ticket) or []
    if orders:
        return orders[0]._asdict()
    return {"error": f"No order found for ticket {ticket}"}


# === Calculations ===

def calc_margin(action: int, symbol: str, volume: float, price: Optional[float] = None):
    """Calculate required margin for an order."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    mt5.symbol_select(symbol)

    if price is None:
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            return None, "Failed to fetch current price"
        price = tick.ask if action == mt5.ORDER_TYPE_BUY else tick.bid

    margin = mt5.order_calc_margin(action, symbol, volume, price)
    if margin is None:
        return None, "MT5 could not calculate margin"
    return margin, None


def calc_profit(action: int, symbol: str, volume: float, price_open: float, price_close: float):
    """Calculate profit for a trade."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    mt5.symbol_select(symbol)

    profit = mt5.order_calc_profit(action, symbol, volume, price_open, price_close)
    if profit is None:
        return None, "MT5 could not calculate profit"
    return profit, None


# === Order Validation & Execution ===

def order_check(request: dict):
    """Validate an order request using `order_check`."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    mt5.symbol_select(request.get("symbol"))

    result = mt5.order_check(request)
    if result is None:
        return None, "MT5 could not validate the order"

    result_dict = result._asdict()
    if hasattr(result, "request") and result.request:
        result_dict["request"] = result.request._asdict()
    return result_dict, None


def order_send(request: dict):
    """Send a trade order using `order_send`."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    mt5.symbol_select(request.get("symbol"))

    # Auto-fetch price if not provided
    if not request.get("price"):
        tick = mt5.symbol_info_tick(request.get("symbol"))
        if not tick:
            return None, "Failed to fetch symbol price"
        if request.get("type") == mt5.ORDER_TYPE_BUY:
            request["price"] = tick.ask
        elif request.get("type") == mt5.ORDER_TYPE_SELL:
            request["price"] = tick.bid
        else:
            return None, "Unsupported order type for price inference"

    result = mt5.order_send(request)
    if result is None:
        return None, "Order send failed: no result returned"

    result_dict = result._asdict()
    if hasattr(result, "request") and result.request:
        result_dict["request"] = result.request._asdict()
    return result_dict, None
