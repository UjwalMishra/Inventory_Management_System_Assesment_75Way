from sqlmodel import Session, select


from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.core.exceptions import AppException


# list all inventories
def get_inventory_service(session: Session):
    return session.exec(select(Inventory)).all()


# creating new inventory
def create_inventory_service(data, session: Session):
    # Validate product
    product = session.get(Product, data.product_id)
    if not product:
        raise AppException("Product not found", status_code=404)

    # Validate warehouse
    warehouse = session.get(Warehouse, data.warehouse_id)
    if not warehouse:
        raise AppException("Warehouse not found", status_code=404)

    # Prevent duplicate inventory row
    existing = session.exec(
        select(Inventory).where(
            Inventory.product_id == data.product_id,
            Inventory.warehouse_id == data.warehouse_id,
        )
    ).first()

    if existing:
        raise AppException(
            "Inventory already exists for this product and warehouse",
            status_code=409,
        )

    inventory = Inventory(**data.dict())
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


# manual adjustment of quantities
def reconcile_inventory_service(
    inventory_id: int,
    quantity: int,
    session: Session,
):
    inventory = session.get(Inventory, inventory_id)

    if not inventory:
        raise AppException("Inventory not found", status_code=404)

    inventory.quantity = quantity
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


# inventory adjustment on sale/purchase
def adjust_inventory_service(
    inventory_id: int,
    action: str,
    quantity: int,
    session: Session,
):
    inventory = session.get(Inventory, inventory_id)

    if not inventory:
        raise AppException("Inventory not found", status_code=404)

    if action == "OUT" and inventory.quantity < quantity:
        raise AppException("Insufficient stock", status_code=400)

    if action == "IN":
        inventory.quantity += quantity
    else:
        inventory.quantity -= quantity
        
    movement = InventoryMovement(
        inventory_id=inventory.id,
        action=action,
        quantity=quantity,
        reason="Stock adjustment",
    )

    session.add(inventory)
    session.add(movement)
    session.commit()
    session.refresh(inventory)

    return {
        "inventory_id": inventory.id,
        "new_quantity": inventory.quantity,
    }

