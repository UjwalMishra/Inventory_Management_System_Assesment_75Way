from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sku: str = Field(unique=True, index=True)
    description: Optional[str] = None
    reorder_level: int
    reorder_quantity: int
