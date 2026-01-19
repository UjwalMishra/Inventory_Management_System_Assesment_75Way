from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.services.report_service import (
    get_low_stock_report,
    get_full_inventory_report,
    get_warehouse_inventory_report,
    export_csv,
    get_inventory_movements,
    get_reorder_preview,
    get_summary_dashboard,
)

router = APIRouter(prefix="/reports", tags=["Reports"])


# low stocks
@router.get("/low-stock")
def low_stock_report(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_low_stock_report(session)


@router.get("/low-stock/export")
def export_low_stock(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    data = get_low_stock_report(session)
    return export_csv(data, "low_stock_report.csv")


# full inventory
@router.get("/inventory")
def inventory_report(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_full_inventory_report(session)


@router.get("/inventory/export")
def export_inventory(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    data = get_full_inventory_report(session)
    return export_csv(data, "inventory_report.csv")


# inventory report of particular warehouse
@router.get("/warehouse/{warehouse_id}")
def warehouse_report(
    warehouse_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_warehouse_inventory_report(warehouse_id, session)


@router.get("/warehouse/{warehouse_id}/export")
def export_warehouse_report(
    warehouse_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    data = get_warehouse_inventory_report(warehouse_id, session)
    return export_csv(
        data["products"],
        f"warehouse_{warehouse_id}_report.csv",
    )


# inventory history
@router.get("/inventory-movements")
def inventory_movements(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_inventory_movements(session)


# reorder suggestion
@router.get("/reorder-preview")
def reorder_preview(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_reorder_preview(session)


# summary dashboard
@router.get("/summary")
def summary_dashboard(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return get_summary_dashboard(session)
