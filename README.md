# FastAPI MT5 Wrapper

A lightweight REST API wrapper for [MetaTrader 5](https://www.metatrader5.com/) built with [FastAPI](https://fastapi.tiangolo.com/).  
This project exposes the official MetaTrader5 Python API as a set of well-documented, structured REST endpoints — making it easier to integrate trading, market data, and account management into your own systems.

---

## ✨ Features

- **Connection Management** – Initialize, reconnect, and shutdown MT5 terminal sessions.
- **Account Information** – Retrieve balance, equity, margin, and login details.
- **Market Data** – List available symbols, get symbol info, and fetch real-time ticks or OHLC data.
- **Positions & Orders** – Inspect open positions, active pending orders, and historical orders/deals.
- **History** – Query trade history by date range and filters.
- **OpenAPI Documentation** – Interactive `/docs` with request/response examples.

---

## 📦 Requirements

- **Python**: 3.10+
- **MetaTrader 5 terminal** installed and configured on the same machine.
- [MetaTrader5 Python package](https://pypi.org/project/MetaTrader5/) (`pip install MetaTrader5`)
- **FastAPI** + **Uvicorn** for serving the API.

---

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/eddipa/fastapi-mt5-wrapper.git
   cd fastapi-mt5-wrapper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` file (see `.env.example` if available):
   ```env
   MT5_PATH="C:/Path/To/terminal64.exe"
   MT5_LOGIN=123456
   MT5_PASSWORD="your-password"
   MT5_SERVER="Broker-ServerName"
   ```

4. **Run the API**
   ```bash
   uvicorn app.main:app --reload
   ```
   API will be available at:
   - Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 📚 API Tags

| Tag         | Description |
|-------------|-------------|
| **system**      | Health & readiness checks, service metadata |
| **connection**  | Initialize, shutdown, and manage MT5 terminal connection |
| **account**     | Retrieve account login, balance, equity, margin |
| **market**      | Symbol list, symbol info, tick data, OHLC candles |
| **positions**   | View and manage open positions |
| **orders**      | Active and historical pending orders |
| **history**     | Trade and deal history queries |

---

## 🛠 Example Usage

**Fetch OHLC data**
```bash
curl "http://127.0.0.1:8000/market/ohlc?symbol=EURUSD&timeframe=M1&count=10"
```

---

## 🧪 Development

Run the app in development mode:
```bash
uvicorn app.main:app --reload
```

Run tests:
```bash
pytest -v
```

Format & lint:
```bash
black .
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 📌 Notes

- This API is a thin wrapper around MetaTrader5’s Python API. You must have the MT5 terminal running for endpoints to work.
- Be cautious with trading endpoints — use a demo account for development/testing.


---

## ⚠️ Disclaimer

This software is provided **as-is** without any warranties.  
Trading foreign exchange (Forex), CFDs, or other financial instruments carries a high level of risk and may not be suitable for all investors.  
You could lose some or all of your invested capital. Always trade responsibly and test thoroughly on a demo account before using this API in live markets.

The author(s) and contributors of this project are **not responsible** for any losses incurred through the use of this software.
