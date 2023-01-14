from sqlalchemy.sql.expression import literal_column

from app.api.models import CreateOrderModel, Order, OrderStatus
from app.db import database, orders


async def get(idempotency_id: int):
    query = orders.select().where(idempotency_id == orders.c.idempotency_id)
    order_db = await database.fetch_one(query=query)
    return Order(**order_db._mapping) if order_db else None


async def create(model: CreateOrderModel):
    order = Order(**{**model.dict(), "status": OrderStatus.CREATED})
    query = orders.insert().values(**order.dict()).returning(literal_column("*"))
    await database.execute(query=query)
    return order


async def update(order: Order, status: str):
    query = orders.update().where(order.id == orders.c.id).values(status=status)
    await database.execute(query=query)
    order.status = status
    return order
