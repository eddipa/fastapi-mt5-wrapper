# app/routers/system.py
from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse, status_code=200)
def healthz():
    # mt5_connected = your_mt5_adapter.is_connected()
    mt5_connected = True
    return HealthResponse(
        app="ok",
        mt5="connected" if mt5_connected else "disconnected",
        time_utc=datetime.now(timezone.utc),
    )
