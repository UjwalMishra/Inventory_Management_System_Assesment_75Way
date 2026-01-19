from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    name: str
    location: str

class WarehouseRead(WarehouseCreate):
    id: int
    is_active: bool
