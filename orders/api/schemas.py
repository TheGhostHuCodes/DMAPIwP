from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Extra, Field  # pylint: disable=no-name-in-module


class SizeEnum(str, Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(str, Enum):
    created = "created"
    progress = "progress"
    canceled = "canceled"
    dispatched = "dispatched"
    delivered = "delivered"
    completed = "completed"


class OrderItemSchema(BaseModel):
    product: str
    size: SizeEnum
    quantity: int = Field(default=1, ge=1)

    class Config:
        extra = Extra.forbid


class CreateOrderSchema(BaseModel):
    order: List[OrderItemSchema]

    class Config:
        extra = Extra.forbid


class GetOrderSchema(CreateOrderSchema):
    id_: UUID = Field(alias="id")
    created: int = Field(description="Date in the form of UNIX timestamp")
    status: StatusEnum
