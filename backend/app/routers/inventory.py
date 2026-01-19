from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
    InventoryAdjust,
)
from app.services.inventory_service import (
    create_inventory_service,
    get_inventory_service,
    reconcile_inventory_service,
    adjust_inventory_service,
)
from app.core.dependencies import require_admin, get_current_user


router = APIRouter(prefix="/inventory", tags=["Inventory"])


# create inventory route - ADMIN only
@router.post("/", dependencies=[Depends(require_admin)], response_model=InventoryRead)
def add_inventory(
    data: InventoryCreate,
    session: Session = Depends(get_session),
):
    return create_inventory_service(data, session)


# get all inventory route
@router.get("/", response_model=list[InventoryRead])
def get_inventory(session: Session = Depends(get_session), user=Depends(get_current_user),):
    return get_inventory_service(session)


# manual adjustments by id - ADMIN only
@router.put("/{inventory_id}", dependencies=[Depends(require_admin)], response_model=InventoryRead)
def update_inventory(
    inventory_id: int,
    data: InventoryUpdate,
    session: Session = Depends(get_session),
):
    return reconcile_inventory_service(
        inventory_id,
        data.quantity,
        session,
    )


# adjust inventory by id - ADMIN only
@router.patch("/{inventory_id}/adjust", dependencies=[Depends(require_admin)],)
def adjust_inventory(
    inventory_id: int,
    data: InventoryAdjust,
    session: Session = Depends(get_session),
):
    return adjust_inventory_service(
        inventory_id,
        data.action,
        data.quantity,
        session,
    )
