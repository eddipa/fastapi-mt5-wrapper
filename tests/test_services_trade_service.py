import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from services.trade_service import TradeService


class TestTradeService(unittest.TestCase):

    def setUp(self):
        patcher = patch("services.trade_service.mt5")
        self.addCleanup(patcher.stop)
        self.mock_mt5 = patcher.start()

        # Ensure initialization always succeeds
        self.mock_mt5.initialize.return_value = True
        self.service = TradeService()

        # Default symbol info
        self.mock_mt5.symbol_info.return_value = MagicMock(
            visible=True,
            trade_mode=self.mock_mt5.SYMBOL_TRADE_MODE_FULL
        )

        self.mock_mt5.symbol_info_tick.return_value = MagicMock(
            bid=1.2000,
            ask=1.2005
        )

        self.mock_mt5.order_send.return_value = MagicMock(
            retcode=self.mock_mt5.TRADE_RETCODE_DONE,
            order=123456,
            price=1.2005,
            volume=0.1,
            comment="Order successful"
        )

    def test_buy_success(self):
        result = self.service.buy(symbol="EURUSD", volume=0.1)
        self.assertEqual(result["retcode_meaning"], "Done")
        self.assertEqual(result["volume"], 0.1)

    def test_sell_success(self):
        result = self.service.sell(symbol="EURUSD", volume=0.1)
        self.assertEqual(result["retcode_meaning"], "Done")
        self.assertEqual(result["volume"], 0.1)

    def test_buy_limit_success(self):
        result = self.service.buy_limit(symbol="EURUSD", volume=0.1, price=1.1990)
        self.assertEqual(result["retcode_meaning"], "Done")

    def test_sell_stop_success(self):
        result = self.service.sell_stop(symbol="EURUSD", volume=0.1, price=1.1980)
        self.assertEqual(result["retcode_meaning"], "Done")

    def test_close_position_success(self):
        # Mock open position
        self.mock_mt5.positions_get.return_value = [
            MagicMock(
                ticket=1001,
                symbol="EURUSD",
                volume=0.1,
                type=self.mock_mt5.ORDER_TYPE_BUY,
                magic=123456
            )
        ]
        result = self.service.close_position(ticket=1001)
        self.assertEqual(result["retcode_meaning"], "Done")

    def test_modify_order_success(self):
        self.mock_mt5.orders_get.return_value = [
            MagicMock(
                ticket=1002,
                sl=1.1900,
                tp=1.2100,
                time_expiration=0
            )
        ]
        self.mock_mt5.order_modify.return_value = True
        result = self.service.modify_order(order_id=1002, new_price=1.2020)
        self.assertEqual(result["status"], "modified")

    def test_symbol_not_found(self):
        self.mock_mt5.symbol_info.return_value = None
        with self.assertRaises(HTTPException) as ctx:
            self.service.buy("FAKE", 0.1)
        self.assertIn("not found", str(ctx.exception.detail))

    def test_order_rejected(self):
        self.mock_mt5.order_send.return_value = MagicMock(
            retcode=self.mock_mt5.TRADE_RETCODE_REJECT,
            comment="Not allowed"
        )
        with self.assertRaises(HTTPException) as ctx:
            self.service.buy("EURUSD", 0.1)
        self.assertIn("Rejected", str(ctx.exception.detail))

    def test_position_not_found(self):
        self.mock_mt5.positions_get.return_value = []
        with self.assertRaises(HTTPException) as ctx:
            self.service.close_position(ticket=99999)
        self.assertIn("Position 99999 not found", str(ctx.exception.detail))

    def test_modify_order_not_found(self):
        self.mock_mt5.orders_get.return_value = []
        with self.assertRaises(HTTPException) as ctx:
            self.service.modify_order(order_id=99999, new_price=1.2500)
        self.assertIn("Order 99999 not found", str(ctx.exception.detail))


if __name__ == "__main__":
    unittest.main()
