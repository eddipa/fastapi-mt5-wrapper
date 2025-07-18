# 📈 MetaTrader 5 FastAPI Wrapper

A FastAPI-based wrapper to interact with MetaTrader 5 (MT5) using Python. This project provides RESTful endpoints for fetching account info, market data, placing trades, and retrieving historical data — ideal for algorithmic trading integrations and quant research workflows.

---

## 🚀 Features

- Initialize and shutdown MT5 terminal connection on app start/stop
- Get account and open positions data
- Retrieve market symbol info and price data
- Submit and close orders via API
- Query historical OHLC data
- Easily extendable FastAPI architecture

---

## 🛠️ Requirements

- Python 3.8+
- MetaTrader 5 

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/mt5-fastapi-wrapper.git
cd mt5-fastapi-wrapper
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Ensure MetaTrader 5 is installed and **logged in** before starting the app. You can customize connection logic in `app/mt5/connection.py`.

---

## ▶️ Running the API

```bash
uvicorn app.main:app --reload
```

Visit the interactive API docs at:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

---

## 🧪 Testing

To test locally:

```bash
curl "http://127.0.0.1:8000/account/"
```

Or use [Postman](https://www.postman.com/) or Swagger UI for quick testing.

🔹 Automated Testing

Unit tests for this project are written using unittest with mock support.

Run all tests:

```bash
python -m unittest discover tests/
```
Or run a specific test file:
```bash
python -m unittest tests/test_trade_service.py
```
Requirements:

    Python ≥ 3.10

    MetaTrader5 (mocked in tests)

    No live MT5 account connection required during testing

---


## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please open issues and submit pull requests to suggest new features, improvements, or bug fixes.

---
