import MetaTrader5 as mt5

def get_open_orders():
    orders = mt5.orders_total() or []
    return {
        "open_orders_count": len(orders),
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

def send_request(symbol: str, 
            order_type: int, volume: float, 
            sl_points: int = 0, tp_points: int = 0, 
            deviation: int = 10, 
            type_time: int = mt5.ORDER_TIME_GTC, 
            type_filling: int = mt5.ORDER_FILLING_RETURN, 
            comment : str = "", magic: int = 12345):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None or not symbol_info.visible:
        raise ValueError(f"Symbol {symbol} not found or not visible.")

    tick = mt5.symbol_info_tick(symbol)
    point = symbol_info.point
    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid # todo: implement other types

    if order_type == mt5.ORDER_TYPE_BUY:
        sl = price - sl_points * point if sl_points != 0 else 0
        tp = price + tp_points * point if tp_points != 0 else 0
    else:
        sl = price + sl_points * point if sl_points != 0 else 0
        tp = price - tp_points * point if tp_points != 0 else 0

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": type_time,
        "type_filling": type_filling,
    }

    result = mt5.order_send(request)
    return result._asdict() if result is not None else {"error": "No response from MT5"}


