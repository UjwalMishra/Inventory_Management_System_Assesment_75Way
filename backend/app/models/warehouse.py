from sqlmodel import SQLModel, Field
from typing import Optional

class Warehouse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    is_active: bool = True
