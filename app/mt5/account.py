import MetaTrader5 as mt5

def get_account_info():
    """
    Retrieve full account information from MetaTrader 5.

    Returns:
        dict or None: A dictionary containing all account fields if successful, else None.
    """
    account = mt5.account_info()
    return account._asdict() if account else None

def get_portfolio_stats():
    """
    Return summarized portfolio statistics including equity, margin, and open positions.

    Returns:
        dict: A dictionary containing portfolio stats such as:
            - balance
            - equity
            - margin
            - free_margin
            - margin_level
            - open_positions_count
            - open_positions_profit
            - open_positions_volume
    Raises:
        RuntimeError: If account info is not available.
    """
    account = mt5.account_info()
    if not account:
        raise RuntimeError("Failed to retrieve account information from MT5.")

    positions = mt5.positions_get() or []
    return {
        "balance": account.balance,
        "equity": account.equity,
        "margin": account.margin,
        "free_margin": account.margin_free,
        "margin_level": account.margin_level,
        "open_positions_count": len(positions),
        "open_positions_profit": sum(pos.profit for pos in positions),
        "open_positions_volume": sum(pos.volume for pos in positions),
    }
