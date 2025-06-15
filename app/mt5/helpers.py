from datetime import datetime


def map_filling_type(code: int) -> str:
    return {
        0: "FOK (Fill or Kill)",
        1: "IOC (Immediate or Cancel)",
        2: "RETURN (Partial allowed)",
        3: "AON (All or None)"
    }.get(code, f"Unknown ({code})")

def map_order_type(code: int) -> str:
    return {
        0: "Buy",
        1: "Sell",
        2: "Buy Limit",
        3: "Sell Limit",
        4: "Buy Stop",
        5: "Sell Stop",
        6: "Buy Stop Limit",
        7: "Sell Stop Limit",
        8: "Close By"
    }.get(code, f"Unknown ({code})")

def map_type_time(code: int) -> str:
    return {
        0: "GTC (Good Till Cancelled)",
        1: "Day",
        2: "Specified",
        3: "Specified Day"
    }.get(code, f"Unknown ({code})")

def map_order_reason(code: int) -> str:
    return {
        0: "Manual",
        1: "Expert",
        2: "Mobile",
        3: "Web",
        4: "Exchange",
        5: "Service"
    }.get(code, f"Unknown ({code})")

def map_order_state(code: int) -> str:
    return {
        0: "Started",
        1: "Placed",
        2: "Canceled",
        3: "Partial",
        4: "Filled",
        5: "Rejected",
        6: "Expired",
        7: "Requested",
        8: "Removed",
        9: "Done"
    }.get(code, f"Unknown ({code})")

def map_deal_type(code: int) -> str:
    return {
        0: "Buy",
        1: "Sell",
        2: "Balance",
        3: "Credit",
        4: "Charge",
        5: "Correction",
        6: "Bonus",
        7: "Commission",
        8: "Commission Daily",
        9: "Commission Monthly",
        10: "Commission Broker",
        11: "Commission Agent",
        12: "Interest",
        13: "Buy Canceled",
        14: "Sell Canceled",
        15: "Dividend",
        16: "Dividend Tax",
        17: "Agent"
    }.get(code, f"Unknown ({code})")

def map_deal_entry(code: int) -> str:
    return {
        0: "In",
        1: "Out",
        2: "In/Out"
    }.get(code, f"Unknown ({code})")

def map_deal_reason(code: int) -> str:
    return {
        0: "Manual",
        1: "Expert",
        2: "Mobile",
        3: "Web",
        4: "Exchange",
        5: "Service"
    }.get(code, f"Unknown ({code})")


def format_expiration(timestamp: int) -> str:
    if timestamp == 0:
        return "None"
    try:
        return datetime.fromtimestamp(timestamp).isoformat()
    except Exception:
        return f"Invalid ({timestamp})"

def format_timestamp(ts: int) -> str:
    if ts <= 0:
        return "None"
    try:
        return datetime.fromtimestamp(ts).isoformat()
    except Exception:
        return f"Invalid ({ts})"