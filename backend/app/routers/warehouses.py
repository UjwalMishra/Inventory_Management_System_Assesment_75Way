from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.schemas.warehouse import WarehouseCreate, WarehouseRead
from app.services.warehouse_service import get_warehouse_with_products
from app.core.dependencies import require_admin, get_current_user
from app.models.warehouse import Warehouse

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


# create warehouse - ADMIN only
@router.post(
    "/",
    dependencies=[Depends(require_admin)],
    response_model=WarehouseRead,
)
def create_warehouse(
    data: WarehouseCreate,
    session: Session = Depends(get_session),
):
    warehouse = Warehouse(**data.dict())
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse


# list all warehouses
@router.get(
    "/",
    response_model=list[WarehouseRead],
)
def get_warehouses(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return session.exec(select(Warehouse)).all()


# warehouse detail + inventory
@router.get("/{warehouse_id}")
def get_warehouse_detail(
    warehouse_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_warehouse_with_products(warehouse_id, session)
