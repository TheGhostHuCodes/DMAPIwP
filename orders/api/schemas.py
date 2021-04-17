from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Extra, Field  # pylint: disable=no-name-in-module


class Size(str, Enum):
    small = "small"
    medium = "medium"
    big = "big"


class Status(str, Enum):
    created = "created"
    progress = "progress"
    canceled = "canceled"
    dispatched = "dispatched"
    delivered = "delivered"
    completed = "completed"


class OrderItem(BaseModel):
    product: str
    size: Size
    quantity: int = Field(default=1, ge=1)

    class Config:
        extra = Extra.forbid


class CreateOrder(BaseModel):
    order: List[OrderItem]

    class Config:
        extra = Extra.forbid


class GetOrder(CreateOrder):
    id_: UUID = Field(alias="id")
    created: int = Field(description="Date in the form of UNIX timestamp")
    status: Status
