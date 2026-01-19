from sqlmodel import Session, select
from app.core.database import engine
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse


def seed_inventory():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        warehouses = session.exec(select(Warehouse)).all()

        if not products or not warehouses:
            print("Seed products and warehouses first")
            return

        for product in products:
            for warehouse in warehouses:
                exists = session.exec(
                    select(Inventory).where(
                        Inventory.product_id == product.id,
                        Inventory.warehouse_id == warehouse.id,
                    )
                ).first()

                if not exists:
                    # intentionally keep some low stock
                    quantity = 3 if product.name == "Laptop" else 25

                    session.add(
                        Inventory(
                            product_id=product.id,
                            warehouse_id=warehouse.id,
                            quantity=quantity,
                        )
                    )

        session.commit()
        print("Inventory seeded")


if __name__ == "__main__":
    seed_inventory()
