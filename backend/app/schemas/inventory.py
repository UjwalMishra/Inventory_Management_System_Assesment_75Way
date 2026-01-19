from pydantic import BaseModel, Field
from typing import Literal


class InventoryCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(ge=0)


class InventoryRead(InventoryCreate):
    id: int


class InventoryUpdate(BaseModel):
    quantity: int


class InventoryAdjust(BaseModel):
    action: Literal["IN", "OUT"]
    quantity: int = Field(gt=0)
