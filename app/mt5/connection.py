import MetaTrader5 as mt5
from app.config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER

def initialize_mt5():
    if not mt5.initialize(
        login=MT5_LOGIN,
        password=MT5_PASSWORD,
        server=MT5_SERVER
    ):
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")

def shutdown_mt5():
    mt5.shutdown()
