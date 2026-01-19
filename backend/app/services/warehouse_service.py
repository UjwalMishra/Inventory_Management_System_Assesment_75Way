from sqlmodel import Session, select
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.product import Product
from app.core.exceptions import AppException


def get_warehouse_with_products(
    warehouse_id: int,
    session: Session,
):
    warehouse = session.get(Warehouse, warehouse_id)

    if not warehouse:
        raise AppException("Warehouse not found", status_code=404)

    inventories = session.exec(
        select(Inventory).where(Inventory.warehouse_id == warehouse_id)
    ).all()

    products_data = []

    for inventory in inventories:
        product = session.get(Product, inventory.product_id)

        products_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "quantity": inventory.quantity,
        })

    return {
        "id": warehouse.id,
        "name": warehouse.name,
        "location": warehouse.location,
        "products": products_data,
    }
