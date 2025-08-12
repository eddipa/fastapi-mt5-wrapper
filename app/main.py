from fastapi import FastAPI
from app.mt5.connection import initialize_mt5, shutdown_mt5
from app.routers import (
    system,
    account,
    terminal,
    symbols,
    market,
    rates,
    ticks,
    positions,
    orders,
    history,
    services,
)


tags_metadata = [
    {
        "name": "system",
        "description": "General service endpoints, including health and readiness checks, and service metadata.",
    },
    # {
    #    "name": "connection",
    #    "description": "MetaTrader 5 terminal connection management — initialize, shutdown, and reconnect.",
    # },
    {
        "name": "account",
        "description": "Retrieve account information such as login, balance, equity, margin, and account status.",
    },
    {
        "name": "market",
        "description": "Access market data — available symbols, symbol info, tick quotes, and OHLC (candlestick) data.",
    },
    # {
    #    "name": "trading",
    #    "description": "Submit, modify, and close orders. Includes market orders, pending orders, and stop/limit orders.",
    # },
    {
        "name": "positions",
        "description": "List and inspect currently open positions, including ticket, volume, price, SL/TP, and profit.",
    },
    {
        "name": "orders",
        "description": "View and manage active pending orders, historical orders, and order history filters.",
    },
    {
        "name": "history",
        "description": "Retrieve trade history and historical deals within a specified time range.",
    },
    # {
    #    "name": "utility",
    #    "description": "Auxiliary tools and calculations — e.g., pip value, margin requirements, and symbol normalization.",
    # },
]

app = FastAPI(
    title="FastAPI MT5 Wrapper",
    version="0.1.1",
    openapi_tags=tags_metadata,
)


@app.on_event("startup")
def startup():
    initialize_mt5()


@app.on_event("shutdown")
def shutdown():
    shutdown_mt5()


app.include_router(account.router, prefix="/system", tags=["system"])
app.include_router(account.router, prefix="/account", tags=["account"])
app.include_router(terminal.router, prefix="/terminal", tags=["terminal"])
app.include_router(symbols.router, prefix="/symbols", tags=["symbols"])
app.include_router(market.router, prefix="/market", tags=["market"])
app.include_router(rates.router, prefix="/rates", tags=["rates"])
app.include_router(ticks.router, prefix="/ticks", tags=["ticks"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(positions.router, prefix="/positions", tags=["positions"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(services.router, prefix="/services", tags=["services"])
