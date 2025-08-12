from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class ErrorResponse(BaseModel):
    error_code: str = Field(..., example="MT5_CONN_FAILED")
    message: str = Field(..., example="MetaTrader 5 terminal not connected.")
    hint: Optional[str] = Field(None, example="Ensure MT5 is open and login is active.")
    correlation_id: Optional[str] = Field(None, example="req_01HXYZ...")


class HealthResponse(BaseModel):
    app: Literal["ok"]
    mt5: Literal["connected", "disconnected"]
    time_utc: datetime
