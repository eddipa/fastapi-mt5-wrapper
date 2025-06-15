from fastapi import APIRouter, HTTPException
from app.mt5 import symbols


router = APIRouter()

@router.get(
    "/symbols",
    summary="Get all available symbols",
    response_description="Retrieve a list of all available trading symbols"
)
def all_symbols():
    """
    Fetch all trading symbols currently available in the MetaTrader 5 terminal.

    Returns:
        JSON object containing:
        - `success`: Whether the fetch was successful.
        - `symbol_count`: Total number of symbols returned.
        - `symbols`: List of symbol names (strings).

    Raises:
        HTTPException: If the symbol list cannot be retrieved.
    """
    data = symbols.get_all_symbols()

    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch symbols")

    return {
        "success": True,
        "symbol_count": len(data),
        "symbols": data
    }

@router.get(
    "/{symbol}",
    summary="Get symbol info",
    response_description="Retrieve detailed information about a specific trading symbol"
)
def symbol_info(symbol: str):
    """
    Fetch detailed metadata and configuration for a given trading symbol.

    Args:
        symbol (str): The symbol name to look up (e.g., 'EURUSD', 'BTCUSD').

    Returns:
        JSON object containing symbol details such as:
        - trading modes
        - volume limits
        - spreads
        - digits
        - margin requirements
        - session data
        - pricing statistics

    Raises:
        HTTPException: If the symbol is not found or data retrieval fails.
    """
    data = symbols.get_symbol_info(symbol)

    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")

    return data

@router.get(
    "/{symbol}/tick",
    summary="Get latest tick data for a symbol",
    response_description="Retrieve the most recent tick data (bid, ask, last price, volume) for a given symbol"
)
def symbol_info_tick(symbol: str):
    """
    Fetch the latest tick information for a specific trading symbol.

    Args:
        symbol (str): The symbol to fetch tick data for (e.g., 'BTCUSD').

    Returns:
        JSON object containing:
        - `time`: Time of the tick (Unix timestamp).
        - `bid`: Current bid price.
        - `ask`: Current ask price.
        - `last`: Last traded price.
        - `volume`: Volume of the last deal.
        - `time_msc`: Tick timestamp in milliseconds.
        - `flags`: Tick flags.
        - `volume_real`: Actual traded volume.

    Raises:
        HTTPException: If the symbol does not exist or no tick data is available.
    """
    data = symbols.get_symbol_info_tick(symbol)

    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' or TICK not found")

    return data

@router.post(
    "/{symbol}/select",
    summary="Select a trading symbol",
    response_description="Make a symbol visible and available for trading operations"
)
def select(symbol: str):
    """
    Selects (activates) a trading symbol in the MetaTrader 5 terminal.

    This is necessary to enable trading or fetching market data for that symbol,
    especially if the symbol is not visible by default.

    Args:
        symbol (str): Symbol to be selected (e.g., 'EURUSD', 'BTCUSD').

    Returns:
        JSON object with a success message indicating the symbol has been selected.

    Raises:
        HTTPException: If the symbol could not be selected (e.g., not found or unavailable).
    """
    if not symbols.select_symbol(symbol):
        raise HTTPException(status_code=500, detail=f"Failed to select {symbol}")

    return {"message": f"Symbol {symbol} selected"}
