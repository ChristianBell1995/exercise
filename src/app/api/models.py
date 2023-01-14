from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, conint, constr, root_validator


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(str, Enum):
    CREATED = "created"
    INACTIVE = "inactive"
    ACTIVE = "active"


class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    idempotency_id: UUID = Field(..., alias="idempotency_id")
    type: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    quantity: conint(gt=0)
    status: OrderStatus
    limit_price_cents: conint(gt=0)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True
        use_enum_values = True


class CreateOrderModel(BaseModel):
    idempotency_id: UUID = Field(..., alias="idempotency_id")
    type: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price_cents: conint(gt=0)
    quantity: conint(gt=0)

    @root_validator
    def validator(cls, values: dict):
        if values.get("type_") == "market" and values.get("limit_price"):
            raise ValueError(
                "Providing a `limit_price` is prohibited for type `market`"
            )

        if values.get("type_") == "limit" and not values.get("limit_price"):
            raise ValueError("Attribute `limit_price` is required for type `limit`")

        return values


class CreateOrderResponseModel(Order):
    pass
