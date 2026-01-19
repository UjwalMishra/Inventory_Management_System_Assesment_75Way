from sqlmodel import Session, select
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory_movement import InventoryMovement
from app.core.exceptions import AppException

import csv
from io import StringIO
from fastapi.responses import StreamingResponse


def _get_low_stock_base(session: Session):
    inventories = session.exec(select(Inventory)).all()
    result = []

    for inventory in inventories:
        product = session.get(Product, inventory.product_id)
        warehouse = session.get(Warehouse, inventory.warehouse_id)

        if inventory.quantity <= product.reorder_level:
            result.append({
                "product": product,
                "warehouse": warehouse,
                "current_stock": inventory.quantity,
            })

    return result



# get products having low stocks service
def get_low_stock_report(session: Session):
    base_data = _get_low_stock_base(session)

    return [
        {
            "product_id": item["product"].id,
            "product_name": item["product"].name,
            "warehouse_id": item["warehouse"].id,
            "warehouse_name": item["warehouse"].name,
            "current_stock": item["current_stock"],
            "reorder_level": item["product"].reorder_level,
            "suggested_reorder_quantity": item["product"].reorder_quantity,
            "reorder_required": True,
        }
        for item in base_data
    ]



# get report of full inventory service
def get_full_inventory_report(session: Session):
    inventories = session.exec(select(Inventory)).all()
    result = []

    for inventory in inventories:
        product = session.get(Product, inventory.product_id)
        warehouse = session.get(Warehouse, inventory.warehouse_id)

        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "quantity": inventory.quantity,
        })

    return result


# get inventory report for specific warehouse service
def get_warehouse_inventory_report(
    warehouse_id: int,
    session: Session,
):
    warehouse = session.get(Warehouse, warehouse_id)
    if not warehouse:
        raise AppException("Warehouse not found", status_code=404)

    inventories = session.exec(
        select(Inventory).where(Inventory.warehouse_id == warehouse_id)
    ).all()

    result = []

    for inventory in inventories:
        product = session.get(Product, inventory.product_id)
        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": inventory.quantity,
        })

    return {
        "warehouse_id": warehouse.id,
        "warehouse_name": warehouse.name,
        "products": result,
    }


# generating csv report service
def export_csv(data: list[dict], filename: str):
    if not data:
        data = []

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys() if data else [])
    writer.writeheader()

    for row in data:
        writer.writerow(row)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )


def get_inventory_movements(session: Session):
    movements = session.exec(select(InventoryMovement)).all()

    return [
        {
            "inventory_id": m.inventory_id,
            "action": m.action,
            "quantity": m.quantity,
            "reason": m.reason,
            "created_at": m.created_at,
        }
        for m in movements
    ]
    
    
# reorder suggestions
def get_reorder_preview(session: Session):
    base_data = _get_low_stock_base(session)

    return [
        {
            "product_id": item["product"].id,
            "product_name": item["product"].name,
            "warehouse_id": item["warehouse"].id,
            "current_stock": item["current_stock"],
            "reorder_quantity": item["product"].reorder_quantity,
            "stock_after_reorder": (
                item["current_stock"] + item["product"].reorder_quantity
            ),
        }
        for item in base_data
    ]




# summary or dashboard
def get_summary_dashboard(session: Session):
    total_products = len(session.exec(select(Product)).all())
    total_warehouses = len(session.exec(select(Warehouse)).all())

    inventories = session.exec(select(Inventory)).all()
    total_stock_units = sum(i.quantity for i in inventories)

    low_stock_items = 0
    for inventory in inventories:
        product = session.get(Product, inventory.product_id)
        if inventory.quantity <= product.reorder_level:
            low_stock_items += 1

    return {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_inventory_units": total_stock_units,
        "low_stock_items": low_stock_items,
    }
