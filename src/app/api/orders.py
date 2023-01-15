import asyncio

from fastapi import APIRouter, HTTPException, status

from app.api import crud, stock_exchange
from app.api.models import CreateOrderModel, CreateOrderResponseModel, OrderStatus
from app.api.stock_exchange import OrderPlacementError

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrderResponseModel,
)
async def create_order(model: CreateOrderModel):
    order = await crud.get(model.idempotency_id)
    if order:
        return order
    order = await crud.create(model=model)

    try:
        await asyncio.to_thread(stock_exchange.place_order, order)
        order = await crud.update(order=order, status=OrderStatus.CREATED)
        return order
    except OrderPlacementError:
        await crud.update(order=order, status=OrderStatus.FAILED)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while placing the order",
        )
