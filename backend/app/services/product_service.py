from sqlmodel import Session, select
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.warehouse import Warehouse
from app.core.exceptions import AppException
from sqlalchemy.exc import IntegrityError

# create product service
def create_product_service(data, session: Session):
    product = Product(**data.dict())

    try:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    except IntegrityError:
        session.rollback()
        raise AppException(
            message="Product with this SKU already exists",
            status_code=409,
        )


# search products with warehouse details
def get_product_with_inventory(
    product_id: int,
    session: Session,
):
    product = session.get(Product, product_id)

    if not product:
        raise AppException("Product not found", status_code=404)

    inventories = session.exec(
        select(Inventory).where(Inventory.product_id == product_id)
    ).all()

    warehouse_data = []

    for inventory in inventories:
        warehouse = session.get(Warehouse, inventory.warehouse_id)

        warehouse_data.append({
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "quantity": inventory.quantity,
        })

    return {
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "description": product.description,
        "reorder_level": product.reorder_level,
        "reorder_quantity": product.reorder_quantity,
        "warehouses": warehouse_data,
    }


# search product by name
def search_products(
    session: Session,
    name: str | None = None,
):
    query = select(Product)

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    products = session.exec(query).all()

    result = []

    for product in products:
        inventories = session.exec(
            select(Inventory).where(Inventory.product_id == product.id)
        ).all()

        warehouse_data = []

        for inventory in inventories:
            warehouse = session.get(Warehouse, inventory.warehouse_id)

            warehouse_data.append({
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "quantity": inventory.quantity,
            })

        result.append({
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "description": product.description,
            "reorder_level": product.reorder_level,
            "reorder_quantity": product.reorder_quantity,
            "warehouses": warehouse_data,
        })

    return result
