from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str | None = None
    reorder_level: int = Field(ge=0)
    reorder_quantity: int = Field(gt=0)

class ProductRead(ProductCreate):
    id: int
