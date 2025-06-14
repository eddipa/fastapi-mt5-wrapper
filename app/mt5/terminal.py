import MetaTrader5 as mt5

def get_terminal_info():
    orders = mt5.terminal_info() or []
    return orders._asdict()

