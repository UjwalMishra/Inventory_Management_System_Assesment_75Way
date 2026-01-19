from sqlmodel import Session, select
from app.core.database import engine
from app.models.warehouse import Warehouse


def seed_warehouses():
    warehouses = [
        {"name": "Chandigarh Warehouse", "location": "Chandigarh"},
        {"name": "Amritsar Warehouse", "location": "Amritsar"},
    ]

    with Session(engine) as session:
        for data in warehouses:
            exists = session.exec(
                select(Warehouse).where(Warehouse.name == data["name"])
            ).first()

            if not exists:
                session.add(Warehouse(**data))

        session.commit()
        print("Warehouses seeded")


if __name__ == "__main__":
    seed_warehouses()
