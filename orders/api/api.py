import time
import uuid
from http import HTTPStatus
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, Response
from starlette import status

from orders.api.schemas import CreateOrderSchema, GetOrderSchema
from orders.app import app

ORDERS: Dict[UUID, Any] = {}


@app.get("/orders", response_model=List[GetOrderSchema])
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    query_set = list(ORDERS.values())
    if cancelled is None and limit is None:
        return query_set

    if cancelled is not None:
        if cancelled:
            query_set = [order for order in query_set if order["status"] == "cancelled"]
        else:
            query_set = [order for order in query_set if order["status"] != "cancelled"]

    if limit is not None and len(query_set) > limit:
        return query_set[:limit]

    return query_set


@app.post("/orders", status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    id_ = uuid.uuid4()
    order["id"] = id_
    order["created"] = time.time()
    order["status"] = "created"
    ORDERS[id_] = order
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    if order_id in ORDERS:
        return ORDERS[order_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    if order_id in ORDERS:
        ORDERS[order_id].update(order_details.dict())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    if order_id in ORDERS:
        del ORDERS[order_id]
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    if order_id in ORDERS:
        ORDERS[order_id]["status"] = "canceled"
        return ORDERS[order_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    if order_id in ORDERS:
        ORDERS[order_id]["status"] = "progress"
        return ORDERS[order_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )
