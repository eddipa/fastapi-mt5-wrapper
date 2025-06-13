import MetaTrader5 as mt5

def get_account_info():
    account = mt5.account_info()
    return account._asdict() if account else None

def get_portfolio_stats():
    account = mt5.account_info()
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