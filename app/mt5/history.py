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
    format_timestamp,
)


# === Orders ===

def get_history_orders_total(from_date: datetime, to_date: datetime):
    """Get total number of historical orders between two dates."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    return mt5.history_orders_total(from_date, to_date), None


def get_history_orders_group(from_date: datetime, to_date: datetime, group: str = None):
    """Get historical orders filtered by optional group name."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    orders = mt5.history_orders_get(from_date, to_date, group) if group else mt5.history_orders_get(from_date, to_date)

    if not orders:
        return [], None

    parsed = []
    for o in orders:
        d = o._asdict()
        d.update({
            "type_readable": map_order_type(d["type"]),
            "type_time_readable": map_type_time(d["type_time"]),
            "type_filling_readable": map_filling_type(d["type_filling"]),
            "reason_readable": map_order_reason(d["reason"]),
            "state_readable": map_order_state(d["state"]),
            "time_setup_readable": format_timestamp(d["time_setup"]),
            "time_expiration_readable": format_timestamp(d.get("time_expiration", 0)),
            "time_done_readable": format_timestamp(d.get("time_done", 0)),
        })
        parsed.append(d)

    return parsed, None


def get_history_order_by_ticket(ticket: int):
    """Get historical order by its ticket number."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    orders = mt5.history_orders_get(ticket=ticket)
    if not orders:
        return None, "No historical order found with ticket"

    parsed = []
    for o in orders:
        d = o._asdict()
        d.update({
            "type_readable": map_order_type(d["type"]),
            "type_time_readable": map_type_time(d["type_time"]),
            "type_filling_readable": map_filling_type(d["type_filling"]),
            "reason_readable": map_order_reason(d["reason"]),
            "state_readable": map_order_state(d["state"]),
            "time_setup_readable": format_timestamp(d["time_setup"]),
            "time_expiration_readable": format_timestamp(d.get("time_expiration", 0)),
            "time_done_readable": format_timestamp(d.get("time_done", 0)),
        })
        parsed.append(d)

    return parsed, None


def get_history_orders_by_position(position_id: int):
    """Get historical orders linked to a specific position ID."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    orders = mt5.history_orders_get(position=position_id)
    if not orders:
        return [], None

    parsed = []
    for o in orders:
        d = o._asdict()
        d.update({
            "type_readable": map_order_type(d["type"]),
            "type_time_readable": map_type_time(d["type_time"]),
            "type_filling_readable": map_filling_type(d["type_filling"]),
            "reason_readable": map_order_reason(d["reason"]),
            "state_readable": map_order_state(d["state"]),
            "time_setup_readable": format_timestamp(d["time_setup"]),
            "time_expiration_readable": format_timestamp(d.get("time_expiration", 0)),
            "time_done_readable": format_timestamp(d.get("time_done", 0)),
        })
        parsed.append(d)

    return parsed, None


# === Deals ===

def get_history_deals_total(from_date: datetime, to_date: datetime):
    """Get total number of historical deals between two dates."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"
    return mt5.history_deals_total(from_date, to_date), None


def get_history_deals_group(from_date: datetime, to_date: datetime, group: str = None):
    """Get historical deals filtered by optional group name."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    deals = mt5.history_deals_get(from_date, to_date, group) if group else mt5.history_deals_get(from_date, to_date)
    if not deals:
        return [], None

    result = []
    for d in deals:
        dd = d._asdict()
        dd.update({
            "type_readable": map_deal_type(dd["type"]),
            "entry_readable": map_deal_entry(dd["entry"]),
            "reason_readable": map_deal_reason(dd["reason"]),
            "time_readable": format_timestamp(dd["time"]),
        })
        result.append(dd)

    return result, None


def get_history_deal_ticket(ticket: int):
    """Get historical deal by its ticket number."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    deal = mt5.history_deals_get(ticket=ticket)
    if not deal:
        return None, "No deal found"

    d = deal[0]._asdict()
    d.update({
        "type_readable": map_deal_type(d["type"]),
        "entry_readable": map_deal_entry(d["entry"]),
        "reason_readable": map_deal_reason(d["reason"]),
        "time_readable": format_timestamp(d["time"]),
    })

    return d, None


def get_history_deals_position(position_id: int):
    """Get historical deals linked to a specific position ID."""
    if not mt5.initialize():
        return None, "Failed to initialize MT5"

    deals = mt5.history_deals_get(position=position_id)
    if not deals:
        return [], None

    result = []
    for d in deals:
        dd = d._asdict()
        dd.update({
            "type_readable": map_deal_type(dd["type"]),
            "entry_readable": map_deal_entry(dd["entry"]),
            "reason_readable": map_deal_reason(dd["reason"]),
            "time_readable": format_timestamp(dd["time"]),
        })
        result.append(dd)

    return result, None
