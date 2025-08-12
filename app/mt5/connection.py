import MetaTrader5 as mt5
from app.config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER

def initialize_mt5():
    """
    Initialize a connection to MetaTrader 5 with credentials from config.

    Raises:
        RuntimeError: If initialization fails, includes the MT5 last error.
    """
    if not mt5.initialize(
        login=MT5_LOGIN,
        password=MT5_PASSWORD,
        server=MT5_SERVER
    ):
        error_code, error_msg = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed [{error_code}]: {error_msg}")

def shutdown_mt5():
    """
    Gracefully shut down the MT5 connection.
    """
    mt5.shutdown()
