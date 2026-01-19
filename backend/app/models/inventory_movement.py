from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class InventoryMovement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_id: int = Field(foreign_key="inventory.id")
    action: str  # IN or OUT
    quantity: int
    reason: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
