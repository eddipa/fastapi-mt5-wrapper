from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import app.mt5.history as history

router = APIRouter()


@router.get(
    "/orders/total/",
    summary="Get total historical orders",
    response_description="Number of historical orders within the given time range",
)
def history_orders_total(
    from_datetime: datetime = Query(
        ..., description="Start datetime (ISO format, e.g. 2024-01-01T00:00:00)"
    ),
    to_datetime: datetime = Query(
        ..., description="End datetime (ISO format, e.g. 2024-12-31T23:59:59)"
    ),
):
    """
    Returns the total number of historical trade orders placed within a specified date range.

    Args:
        from_datetime (datetime): The start of the time range (inclusive).
        to_datetime (datetime): The end of the time range (inclusive).

    Returns:
        JSON response with:
        - `success`: Whether the operation succeeded.
        - `from`: Start of the range (ISO format).
        - `to`: End of the range (ISO format).
        - `order_count`: Number of historical orders.

    Raises:
        HTTPException: If MT5 initialization or data fetch fails.
    """
    total, error = history.get_history_orders_total(from_datetime, to_datetime)

    if total is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "order_count": total,
    }


@router.get(
    "/orders/",
    summary="Fetch historical trade orders",
    response_description="A list of historical trade orders within the specified range and optional symbol group",
)
def get_filtered_orders(
    from_datetime: datetime = Query(
        ..., description="Start datetime (ISO format, e.g. 2024-01-01T00:00:00)"
    ),
    to_datetime: datetime = Query(
        ..., description="End datetime (ISO format, e.g. 2024-12-31T23:59:59)"
    ),
    group: Optional[str] = Query(
        None, description="Symbol group filter (e.g. '*BTC*', '*USD*')"
    ),
):
    """
    Fetches historical trade orders from MetaTrader 5 within a given time range.

    Optionally filters by a symbol group (e.g. all orders involving BTC or USD pairs).

    Args:
        from_datetime (datetime): Start of the date range (inclusive).
        to_datetime (datetime): End of the date range (inclusive).
        group (str, optional): A string to filter by symbol group (wildcards supported).

    Returns:
        JSON response with:
        - `success`: Whether the query succeeded.
        - `from`, `to`: The time range used.
        - `group`: The filter applied (if any).
        - `order_count`: Number of matching orders.
        - `orders`: List of historical order objects.

    Raises:
        HTTPException: If MT5 connection or data retrieval fails.
    """
    orders, error = history.get_history_orders_group(from_datetime, to_datetime, group)

    if orders is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "group": group,
        "order_count": len(orders),
        "orders": orders,
    }


@router.get(
    "/orders/{ticket}",
    summary="Get historical order by ticket",
    response_description="Details of a specific historical order",
)
def get_order_by_ticket(ticket: int):
    """
    Fetch a single historical order by its unique ticket number.

    Args:
        ticket (int): The unique ID of the historical order.

    Returns:
        JSON response containing:
        - `success`: Boolean indicating the result status.
        - `ticket`: The queried order ticket number.
        - `order`: A dictionary of the order details.

    Raises:
        HTTPException: If the order is not found or MT5 fails to return a result.
    """
    order, error = history.get_history_order_by_ticket(ticket)

    if order is None:
        raise HTTPException(status_code=404, detail=error)

    return {"success": True, "ticket": ticket, "order": order}


@router.get(
    "/orders/position/{position_id}",
    summary="Get all orders linked to a position",
    response_description="Historical orders associated with a given position ID",
)
def get_orders_by_position(position_id: int):
    """
    Retrieve all historical trade orders that are associated with a specific position.

    Args:
        position_id (int): The unique position ID used to match related orders.

    Returns:
        JSON response containing:
        - `success`: Boolean indicating if the query succeeded.
        - `position_id`: The queried position ID.
        - `order_count`: Number of matching orders.
        - `orders`: List of historical orders associated with the position.

    Raises:
        HTTPException: If no orders are found or an error occurs during the request.
    """
    orders, error = history.get_history_orders_by_position(position_id)

    if orders is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "position_id": position_id,
        "order_count": len(orders),
        "orders": orders,
    }


@router.get(
    "/deals/total/",
    summary="Get total number of historical deals",
    response_description="Count of historical trade deals in the specified date range",
)
def history_deals_total(
    from_datetime: datetime = Query(
        ..., description="Start datetime (ISO format, e.g. 2024-01-01T00:00:00)"
    ),
    to_datetime: datetime = Query(
        ..., description="End datetime (ISO format, e.g. 2024-12-31T23:59:59)"
    ),
):
    """
    Fetch the total number of historical trade deals within a specified time range from MetaTrader 5.

    Args:
        from_datetime (datetime): The start datetime of the range (inclusive).
        to_datetime (datetime): The end datetime of the range (inclusive).

    Returns:
        JSON object containing:
        - `success`: True if the query was successful.
        - `from`: The requested start datetime (ISO format).
        - `to`: The requested end datetime (ISO format).
        - `deal_count`: Number of trade deals during the given period.

    Raises:
        HTTPException: If initialization fails or no data is returned from MT5.
    """
    total, error = history.get_history_deals_total(from_datetime, to_datetime)

    if total is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "deal_count": total,
    }


@router.get(
    "/deals/group/",
    summary="Fetch historical deals by symbol group",
    response_description="List of trade deals filtered by symbol group within a specified time range",
)
def get_filtered_deals(
    from_datetime: datetime = Query(
        ..., description="Start datetime (ISO format, e.g. 2024-01-01T00:00:00)"
    ),
    to_datetime: datetime = Query(
        ..., description="End datetime (ISO format, e.g. 2024-12-31T23:59:59)"
    ),
    group: Optional[str] = Query(
        None, description="Symbol group filter (wildcards supported, e.g. '*BTC*')"
    ),
):
    """
    Retrieve historical trade deals from MetaTrader 5 that occurred within a given time range,
    optionally filtered by a symbol group (e.g. all BTC-related symbols).

    Args:
        from_datetime (datetime): Start of the time window (inclusive).
        to_datetime (datetime): End of the time window (inclusive).
        group (Optional[str]): Wildcard-enabled filter string for symbols (e.g. '*USD*').

    Returns:
        JSON object containing:
        - `success`: Indicates if the query was successful.
        - `from`: Start datetime in ISO format.
        - `to`: End datetime in ISO format.
        - `group`: Applied symbol filter (if any).
        - `deal_count`: Number of matching deals.
        - `deals`: List of deal records returned from MT5.

    Raises:
        HTTPException: If the MT5 request fails or no data is returned.
    """
    deals, error = history.get_history_deals_group(from_datetime, to_datetime, group)

    if deals is None:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "from": from_datetime.isoformat(),
        "to": to_datetime.isoformat(),
        "group": group,
        "deal_count": len(deals),
        "deals": deals,
    }


@router.get(
    "/deals/{ticket}",
    summary="Get historical deal by ticket",
    response_description="Details of a specific trade deal",
)
def get_deal_by_ticket(ticket: int):
    """
    Retrieve a specific historical deal from MetaTrader 5 using its ticket number.

    Args:
        ticket (int): The unique ID of the deal to retrieve.

    Returns:
        JSON response with:
        - `success`: Whether the request succeeded.
        - `ticket`: The ticket ID used for the query.
        - `deal`: A dictionary containing the deal details.

    Raises:
        HTTPException: If the deal is not found or MT5 fails to return data.
    """
    deal, error = history.get_history_deal_ticket(ticket)

    if deal is None:
        raise HTTPException(status_code=404, detail=error)

    return {"success": True, "ticket": ticket, "deal": deal}


@router.get(
    "/deals/position/{position_id}",
    summary="Get historical deals for a position",
    response_description="List of trade deals associated with a specific position ID",
)
def get_deals_by_position(position_id: int):
    """
    Retrieve all historical trade deals associated with a given position ID.

    Args:
        position_id (int): The unique position ID used to match related deals.

    Returns:
        JSON response containing:
        - `success`: Indicates if the query was successful.
        - `position_id`: The queried position ID.
        - `deal_count`: Number of matching deals.
        - `deals`: List of deal records related to the position.

    Raises:
        HTTPException: If the query fails or no deals are found.
    """
    deals, error = history.get_history_deals_position(position_id)

    if deals is None:
        raise HTTPException(status_code=404, detail=error)

    return {
        "success": True,
        "position_id": position_id,
        "deal_count": len(deals),
        "deals": deals,
    }
