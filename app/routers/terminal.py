from fastapi import APIRouter, HTTPException

from app.mt5 import terminal

router = APIRouter()

@router.get(
    "/info/",
    summary="Get MetaTrader 5 terminal info",
    response_description="Retrieve information about the currently running MT5 terminal instance"
)
def get_terminal():
    """
    Returns metadata about the MetaTrader 5 terminal environment.

    This includes details such as:
    - Build version
    - Path to the terminal executable
    - Data directory
    - Community account
    - Trade server connection details

    Returns:
        JSON object with terminal information fields.

    Raises:
        HTTPException: Not raised explicitly, but errors can occur if MT5 is not running or not initialized.
    """
    return terminal.get_terminal_info()
