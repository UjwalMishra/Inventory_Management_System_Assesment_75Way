from sqlmodel import Session, select
from app.core.database import engine
from app.models.product import Product


def seed_products():
    products = [
        {
            "name": "Laptop",
            "sku": "LAP-001",
            "description": "Business laptop",
            "reorder_level": 5,
            "reorder_quantity": 10,
        },
        {
            "name": "Bottle",
            "sku": "BOT-001",
            "description": "Water bottle",
            "reorder_level": 20,
            "reorder_quantity": 50,
        },
        {
            "name": "Iphone",
            "sku": "IPHN-001",
            "description": "Iphone 16",
            "reorder_level": 10,
            "reorder_quantity": 30,
        },
    ]

    with Session(engine) as session:
        for data in products:
            exists = session.exec(
                select(Product).where(Product.sku == data["sku"])
            ).first()

            if not exists:
                session.add(Product(**data))

        session.commit()
        print("Products seeded")


if __name__ == "__main__":
    seed_products()
