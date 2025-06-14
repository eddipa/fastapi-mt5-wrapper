from fastapi import FastAPI
from app.mt5.connection import initialize_mt5, shutdown_mt5
from app.routers import account, terminal, symbols, market, positions, orders, trading, history

app = FastAPI()

@app.on_event("startup")
def startup():
    initialize_mt5()

@app.on_event("shutdown")
def shutdown():
    shutdown_mt5()


app.include_router(account.router, prefix="/account")
app.include_router(terminal.router, prefix="/terminal")
app.include_router(symbols.router, prefix="/symbols")
app.include_router(market.router, prefix="/market")
app.include_router(positions.router, prefix="/positions")
app.include_router(orders.router, prefix="/orders")
#app.include_router(trading.router, prefix="/trade")
#app.include_router(history.router, prefix="/history")
