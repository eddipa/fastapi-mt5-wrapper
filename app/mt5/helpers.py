from datetime import datetime


# === Trading Mode & Account Mappings ===

def map_trade_mode(code: int) -> str:
    """Map trade mode code to human-readable string."""
    return {
        0: "Disabled",
        1: "Long Only",
        2: "Short Only",
        3: "Close Only",
        4: "Full Access"
    }.get(code, f"Unknown ({code})")

def map_calc_mode(code: int) -> str:
    """Map calculation mode for symbol margin requirements."""
    return {
        0: "Forex",
        1: "CFD",
        2: "Futures",
        3: "CFD Index",
        4: "CFD Leverage",
        5: "Exchange Stocks",
        6: "Exchange Futures",
        7: "CFD Forex",
        8: "CFD Crypto",
    }.get(code, f"Unknown ({code})")

def map_exemode(code: int) -> str:
    """Map execution mode for orders."""
    return {
        0: "Request",
        1: "Instant",
        2: "Market",
        3: "Exchange"
    }.get(code, f"Unknown ({code})")

def map_filling_type(code: int) -> str:
    """Map order filling type."""
    return {
        0: "FOK (Fill or Kill)",
        1: "IOC (Immediate or Cancel)",
        2: "RETURN (Partial allowed)",
        3: "AON (All or None)"
    }.get(code, f"Unknown ({code})")

# === Orders ===

def map_order_type(code: int) -> str:
    """Map order type code to readable name."""
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
    """Map order expiration type."""
    return {
        0: "GTC (Good Till Cancelled)",
        1: "Day",
        2: "Specified",
        3: "Specified Day"
    }.get(code, f"Unknown ({code})")

def map_order_reason(code: int) -> str:
    """Map reason why an order was placed."""
    return {
        0: "Manual",
        1: "Expert",
        2: "Mobile",
        3: "Web",
        4: "Exchange",
        5: "Service"
    }.get(code, f"Unknown ({code})")

def map_order_state(code: int) -> str:
    """Map the current state of an order."""
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

# === Deals ===

def map_deal_type(code: int) -> str:
    """Map deal type (Buy/Sell/Commission/etc)."""
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
    """Map deal entry direction (In/Out/Both)."""
    return {
        0: "In",
        1: "Out",
        2: "In/Out"
    }.get(code, f"Unknown ({code})")

def map_deal_reason(code: int) -> str:
    """Map reason why a deal was executed."""
    return {
        0: "Manual",
        1: "Expert",
        2: "Mobile",
        3: "Web",
        4: "Exchange",
        5: "Service"
    }.get(code, f"Unknown ({code})")

# === Formatters ===

def format_expiration(timestamp: int) -> str:
    """Format expiration timestamp to ISO format."""
    if timestamp == 0:
        return "None"
    try:
        return datetime.fromtimestamp(timestamp).isoformat()
    except Exception:
        return f"Invalid ({timestamp})"

def format_timestamp(ts: int) -> str:
    """Format general timestamp to ISO format."""
    if ts <= 0:
        return "None"
    try:
        return datetime.fromtimestamp(ts).isoformat()
    except Exception:
        return f"Invalid ({ts})"

def decode_tick_flags(flags: int) -> list[str]:
    """
    Decode tick flags from MarketInfo.

    Args:
        flags (int): Integer flag bitmask

    Returns:
        list[str]: List of changed fields
    """
    mapping = {
        1: "Bid Changed",
        2: "Ask Changed",
        4: "Last Changed",
        8: "Volume Changed",
    }
    return [label for bit, label in mapping.items() if flags & bit]
