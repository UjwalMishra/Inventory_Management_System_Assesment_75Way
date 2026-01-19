from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from app.core.security import hash_password


def seed_admin():
    with Session(engine) as session:
        existing_admin = session.exec(
            select(User).where(User.username == "admin")
        ).first()

        if existing_admin:
            print("Admin user already exists")
            return

        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin",
        )

        session.add(admin)
        session.commit()
        print("Admin user created successfully")


if __name__ == "__main__":
    seed_admin()
