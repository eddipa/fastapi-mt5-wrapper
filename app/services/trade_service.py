import MetaTrader5 as mt5
from fastapi import HTTPException
import logging

logger = logging.getLogger("mt5_trade_service")


class TradeService:
    """
    A Python wrapper around MetaTrader 5 trade functions, inspired by MQL5's CTrade class.
    Provides methods to execute market orders, place pending orders, close positions, and modify orders.
    """

    def __init__(self):
        """
        Initializes the MT5 connection when the service is instantiated.
        """
        if not mt5.initialize():
            raise RuntimeError("Failed to initialize MetaTrader 5")

    def _check_connection(self):
        """
        Ensures MT5 is initialized before every trade operation.
        Raises:
            HTTPException: If connection to MT5 fails.
        """
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="MT5 connection failed")

    def _validate_symbol(self, symbol: str):
        """
        Validates if the symbol exists, is visible, and is tradable.
        Args:
            symbol (str): The trading symbol to validate (e.g., 'EURUSD').
        Raises:
            HTTPException: If the symbol is invalid or not tradable.
        Returns:
            SymbolInfo: The validated symbol info object.
        """
        info = mt5.symbol_info(symbol)
        if info is None:
            raise HTTPException(status_code=400, detail=f"Symbol '{symbol}' not found")
        if not info.visible and not mt5.symbol_select(symbol, True):
            raise HTTPException(status_code=400, detail=f"Symbol '{symbol}' could not be selected")
        if info.trade_mode not in [
            mt5.SYMBOL_TRADE_MODE_FULL,
            mt5.SYMBOL_TRADE_MODE_LONGONLY,
            mt5.SYMBOL_TRADE_MODE_SHORTONLY,
        ]:
            raise HTTPException(status_code=400, detail=f"Symbol '{symbol}' is not tradable")
        return info

    def _retcode_meaning(self, retcode: int) -> str:
        """
        Maps MT5 return codes to human-readable explanations.
        Args:
            retcode (int): MT5 return code.
        Returns:
            str: Explanation of the return code.
        """
        return {
            mt5.TRADE_RETCODE_DONE: "Done",
            mt5.TRADE_RETCODE_REQUOTE: "Requote",
            mt5.TRADE_RETCODE_REJECT: "Rejected",
            mt5.TRADE_RETCODE_INVALID: "Invalid request",
            mt5.TRADE_RETCODE_NOT_ENOUGH_MONEY: "Not enough funds",
            mt5.TRADE_RETCODE_INVALID_VOLUME: "Invalid volume",
            mt5.TRADE_RETCODE_MARKET_CLOSED: "Market closed",
            mt5.TRADE_RETCODE_PRICE_CHANGED: "Price changed",
            mt5.TRADE_RETCODE_NO_CONNECTION: "No connection",
            mt5.TRADE_RETCODE_SERVER_BUSY: "Server busy",
            mt5.TRADE_RETCODE_TRADE_DISABLED: "Trading disabled",
        }.get(retcode, "Unknown error")

    def _handle_result(self, result):
        """
        Handles the result of an MT5 order_send() call.
        Raises:
            HTTPException: If trade execution failed.
        Returns:
            dict: Structured response from the trade operation.
        """
        if result is None:
            raise HTTPException(status_code=500, detail="No response from MT5")

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            msg = f"Trade failed: {result.retcode} - {self._retcode_meaning(result.retcode)}"
            logger.warning(msg + f" | comment: {result.comment}")
            raise HTTPException(status_code=400, detail=msg)

        return {
            "retcode": result.retcode,
            "retcode_meaning": self._retcode_meaning(result.retcode),
            "order": result.order,
            "price": result.price,
            "volume": result.volume,
            "comment": result.comment,
        }

    # === Market Orders ===

    def buy(self, symbol: str, volume: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Executes a market buy order.
        """
        self._check_connection()
        self._validate_symbol(symbol)
        price = mt5.symbol_info_tick(symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    def sell(self, symbol: str, volume: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Executes a market sell order.
        """
        self._check_connection()
        self._validate_symbol(symbol)
        price = mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    # === Pending Orders ===

    def buy_limit(self, symbol: str, volume: float, price: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Places a Buy Limit order at a specified price.
        """
        self._check_connection()
        self._validate_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    def sell_limit(self, symbol: str, volume: float, price: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Places a Sell Limit order at a specified price.
        """
        self._check_connection()
        self._validate_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    def buy_stop(self, symbol: str, volume: float, price: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Places a Buy Stop order above the current price.
        """
        self._check_connection()
        self._validate_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    def sell_stop(self, symbol: str, volume: float, price: float, sl=None, tp=None, deviation=10, magic=0):
        """
        Places a Sell Stop order below the current price.
        """
        self._check_connection()
        self._validate_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_STOP,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    # === Close / Modify ===

    def close_position(self, ticket: int):
        """
        Closes an open position by ticket ID.
        Args:
            ticket (int): The position ticket to close.
        Returns:
            dict: Result of the close operation.
        """
        self._check_connection()
        position = mt5.positions_get(ticket=ticket)
        if not position:
            raise HTTPException(status_code=404, detail=f"Position {ticket} not found")

        pos = position[0]
        tick = mt5.symbol_info_tick(pos.symbol)
        price = tick.bid if pos.type == mt5.ORDER_TYPE_BUY else tick.ask
        close_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 10,
            "magic": pos.magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return self._handle_result(mt5.order_send(request))

    def modify_order(self, order_id: int, new_price: float, new_sl=None, new_tp=None):
        """
        Modifies a pending order (price, SL/TP).
        Args:
            order_id (int): The ticket of the order to modify.
            new_price (float): New desired order price.
            new_sl (float, optional): New Stop Loss price.
            new_tp (float, optional): New Take Profit price.
        Returns:
            dict: Result of the modification.
        """
        self._check_connection()
        order = mt5.orders_get(ticket=order_id)
        if not order:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

        o = order[0]
        result = mt5.order_modify(
            ticket=o.ticket,
            price=new_price,
            sl=new_sl if new_sl is not None else o.sl,
            tp=new_tp if new_tp is not None else o.tp,
            expiration=o.time_expiration,
        )

        if not result:
            raise HTTPException(status_code=400, detail=f"Failed to modify order {order_id}")

        return {"status": "modified", "ticket": o.ticket}
