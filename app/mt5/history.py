import MetaTrader5 as mt5
from datetime import datetime

from app.mt5.helpers import (
    map_order_type,
    map_filling_type,
    map_type_time,
    map_order_reason,
    map_order_state,
    map_deal_type,
    map_deal_entry,
    map_deal_reason,
    format_expiration,
    format_timestamp,
)

def get_history_orders_total(from_date: datetime, to_date: datetime):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    total = mt5.history_orders_total(from_date, to_date)

    return total, None

def get_history_orders_group(from_date: datetime, to_date: datetime, group: str = None):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    if group:
        orders = mt5.history_orders_get(from_date, to_date, group)
    else:
        orders = mt5.history_orders_get(from_date, to_date)

    if orders is None or len(orders) == 0:
        return [], None

    # Convert each to dict and add human-readable field
    parsed = []
    for o in orders:
        d = o._asdict()
        d["type_readable"] = map_order_type(d["type"])
        d["type_time_readable"] = map_type_time(d["type_time"])
        d["type_filling_readable"] = map_filling_type(d["type_filling"])
        d["reason_readable"] = map_order_reason(d["reason"])
        d["state_readable"] = map_order_state(d["state"])
        d["time_setup_readable"] = format_timestamp(d["time_setup"])
        d["time_expiration_readable"] = format_timestamp(d.get("time_expiration", 0))
        d["time_done_readable"] = format_timestamp(d.get("time_done", 0))
        parsed.append(d)

    return parsed, None

def get_history_order_by_ticket(ticket: int):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    order = mt5.history_orders_get(ticket=ticket)

    if order is None or len(order) == 0:
        return None, "No historical order found with ticket"

    # Convert each to dict and add human-readable field
    parsed = []
    for o in orders:
        d = o._asdict()
        d["type_readable"] = map_order_type(d["type"])
        d["type_time_readable"] = map_type_time(d["type_time"])
        d["type_filling_readable"] = map_filling_type(d["type_filling"])
        d["reason_readable"] = map_order_reason(d["reason"])
        d["state_readable"] = map_order_state(d["state"])
        d["time_setup_readable"] = format_timestamp(d["time_setup"])
        d["time_expiration_readable"] = format_timestamp(d.get("time_expiration", 0))
        d["time_done_readable"] = format_timestamp(d.get("time_done", 0))
        parsed.append(d)

    return parsed, None

def get_history_orders_by_position(position_id: int):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    orders = mt5.history_orders_get(position=position_id)

    if orders is None or len(orders) == 0:
        return [], None
    
    # Convert each to dict and add human-readable field
    parsed = []
    for o in orders:
        d = o._asdict()
        d["type_readable"] = map_order_type(d["type"])
        d["type_time_readable"] = map_type_time(d["type_time"])
        d["type_filling_readable"] = map_filling_type(d["type_filling"])
        d["reason_readable"] = map_order_reason(d["reason"])
        d["state_readable"] = map_order_state(d["state"])
        d["time_setup_readable"] = format_timestamp(d["time_setup"])
        d["time_expiration_readable"] = format_timestamp(d.get("time_expiration", 0))
        d["time_done_readable"] = format_timestamp(d.get("time_done", 0))
        parsed.append(d)

    return parsed, None
    
def get_history_deals_total(from_date: datetime, to_date: datetime):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    total = mt5.history_deals_total(from_date, to_date)

    return total, None

def get_history_deals_group(from_date: datetime, to_date: datetime, group: str = None):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    if group:
        deals = mt5.history_deals_get(from_date, to_date, group)
    else:
        deals = mt5.history_deals_get(from_date, to_date)

    if deals is None or len(deals) == 0:
        return [], None

    result = []
    for d in deals:
        dd = d._asdict()
        dd["type_readable"] = map_deal_type(dd["type"])
        dd["entry_readable"] = map_deal_entry(dd["entry"])
        dd["reason_readable"] = map_deal_reason(dd["reason"])
        dd["time_readable"] = format_timestamp(dd["time"])
        result.append(dd)

    return result, None

def get_history_deal_ticket(ticket: int):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    deal = mt5.history_deals_get(ticket=ticket)

    if deal is None or len(deal) == 0:
        return None, "No deal found"

    d = deal[0]._asdict()
    d["type_readable"] = map_deal_type(d["type"])
    d["entry_readable"] = map_deal_entry(d["entry"])
    d["reason_readable"] = map_deal_reason(d["reason"])
    d["time_readable"] = format_timestamp(d["time"])

    return d, None


def get_history_deals_position(position_id: int):
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    deals = mt5.history_deals_get(position=position_id)

    if deals is None or len(deals) == 0:
        return [], None

    result = []
    for d in deals:
        dd = d._asdict()
        dd["type_readable"] = map_deal_type(dd["type"])
        dd["entry_readable"] = map_deal_entry(dd["entry"])
        dd["reason_readable"] = map_deal_reason(dd["reason"])
        dd["time_readable"] = format_timestamp(dd["time"])
        result.append(dd)

    return result, None