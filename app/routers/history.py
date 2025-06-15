from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import app.mt5.history as history

router = APIRouter()

@router.get("/orders/total/")
def history_orders_total(
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)")
):
    total, error = history.get_history_orders_total(from_datetime, to_datetime)

    if total is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "order_count": total
    }

@router.get("/orders/")
def get_filtered_orders(
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    group: str = Query(None, description="Symbol filter (e.g. '*BTC*')")
):
    orders, error = history.get_history_orders_group(from_datetime, to_datetime, group)

    if orders is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "group": group,
        "order_count": len(orders),
        "orders": orders
    }

@router.get("/orders/{ticket}")
def get_order_by_ticket(ticket: int):
    order, error = history.get_history_order_by_ticket(ticket)

    if order is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "ticket": ticket,
        "order": order
    }

@router.get("/orders/position/{position_id}")
def get_orders_by_position(position_id: int):
    orders, error = history.get_history_orders_by_position(position_id)

    if orders is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "position_id": position_id,
        "order_count": len(orders),
        "orders": orders
    }

@router.get("/deals/total/")
def history_deals_total(
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)")
):
    total, error = history.get_history_deals_total(from_datetime, to_datetime)

    if total is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "deal_count": total
    }

@router.get("/deals/group/")
def get_filtered_deals(
    from_datetime: datetime = Query(..., description="Start datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    to_datetime: datetime = Query(..., description="End datetime in ISO format (e.g. 2024-01-01T00:00:00)"),
    group: str = Query(None, description="Symbol filter (e.g. '*BTC*')")
):
    deals, error = history.get_history_deals_group(from_datetime, to_datetime, group)

    if deals is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "group": group,
        "deal_count": len(deals),
        "deals": deals
    }

@router.get("/deals/{ticket}")
def get_deal_by_ticket(ticket: int):
    deal, error = history.get_history_deal_ticket(ticket)

    if deal is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "ticket": ticket,
        "deal": deal
    }

@router.get("/deals/position/{position_id}")
def get_deals_by_position(position_id: int):
    deals, error = history.get_history_deals_position(position_id)

    if deals is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "position_id": position_id,
        "deal_count": len(deals),
        "deals": deals
    }