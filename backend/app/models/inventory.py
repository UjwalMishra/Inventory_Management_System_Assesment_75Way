from sqlmodel import SQLModel, Field
from typing import Optional

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    quantity: int
