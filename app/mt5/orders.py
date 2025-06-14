import MetaTrader5 as mt5


RET_CODE_MAP = {
    0: "Request executed successfully",
    1: "Request executed partially",
    10004: "Trade server busy",
    10006: "No connection to trade server",
    10007: "Operation is allowed only for live accounts",
    10008: "Request processing timeout",
    10009: "Invalid request",
    10010: "Invalid volume",
    10011: "Invalid price",
    10012: "Invalid stop",
    10013: "Trade is disabled",
    10014: "Market is closed",
    10015: "Trade timeout",
    10016: "Invalid order",
    10017: "Trade context busy",
    10018: "Trade expiration denied",
    10019: "Too many requests",
    10020: "Order not found",
    10021: "Unknown symbol",
    10022: "Server busy",
    10023: "Trade modification failed",
    10024: "Too frequent requests",
    10025: "Order locked",
    10026: "Long positions only allowed",
    10027: "Too many pending orders",
    10028: "Hedge is prohibited",
    10029: "Close by orders prohibited"
    # Add more as needed from MT5 docs
}

def parse_order_retcode(retcode: int) -> str:
    return RET_CODE_MAP.get(retcode, "Unknown retcode")


def get_orders():
    orders = mt5.orders_total() or 0
    return {
        "orders_count": orders
    }

def get_open_orders_from_symbol(symbol: str):
    orders = mt5.orders_get(symbol=symbol) or []

    orders_dict = {}

    for counter, o in enumerate(orders):
        order = o._asdict()
        orders_dict[counter] = order
    
    return {
        "open_orders_count": len(orders),
        "open_orders_volume": sum(order.volume for order in orders),
        "orders": orders_dict
    }

def get_open_orders_by_group(group: str):
    orders = mt5.orders_get(group=group) or []

    orders_dict = {}

    for counter, o in enumerate(orders):
        order = o._asdict()
        orders_dict[counter] = order
    
    return {
        "open_orders_count": len(orders),
        "open_orders_volume": sum(order.volume for order in orders),
        "orders": orders_dict
    }

def get_open_order_by_ticket(ticket: int):
    orders = mt5.orders_get(ticket=ticket) or []
    if orders:  # not None and not empty
        return orders[0]._asdict()
    else:
        return {"error": f"No order found for ticket {ticket}"}

def calc_margin(action: int, symbol: str, volume: float, price: float = None):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    mt5.symbol_select(symbol)

    # Auto-fetch price if not provided
    if price is None:
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None, "Failed to fetch current price"
        if action == mt5.ORDER_TYPE_BUY:
            price = tick.ask
        elif action == mt5.ORDER_TYPE_SELL:
            price = tick.bid
        else:
            return None, "Unsupported action for price inference"

    margin = mt5.order_calc_margin(action, symbol, volume, price)

    if margin is None:
        return None, "MT5 could not calculate margin"

    return margin, None

def calc_profit(action: int, symbol: str, volume: float, price_open: float, price_close: float):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    mt5.symbol_select(symbol)

    profit = mt5.order_calc_profit(action, symbol, volume, price_open, price_close)

    if profit is None:
        return None, "MT5 could not calculate profit"

    return profit, None

def order_check(request: dict):
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
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    mt5.symbol_select(request.get("symbol"))

    # Auto-fill price if missing 
    if not request.get("price"):
        tick = mt5.symbol_info_tick(request.get("symbol"))
        if not tick:
            return None, "Failed to fetch symbol price"

    result = mt5.order_send(request)

    if result is None:
        return None, "Order send failed: no result returned"
    
    result_dict = result._asdict()
    if hasattr(result, "request") and result.request:
        result_dict["request"] = result.request._asdict()

    return result_dict, None