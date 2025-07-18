import MetaTrader5 as mt5

def get_terminal_info():
    """
    Retrieve MetaTrader 5 terminal information.

    Returns:
        dict or None: Terminal info as a dictionary, or None if retrieval fails.
    """
    info = mt5.terminal_info()
    return info._asdict() if info else None
