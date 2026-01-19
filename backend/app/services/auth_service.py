from sqlmodel import Session, select
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.exceptions import AppException
from app.core.security import hash_password


# login
def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if not user or not verify_password(password, user.password_hash):
        raise AppException("Invalid credentials", status_code=401)

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role,
    })

    return token


# signup
def signup_user(
    username: str,
    password: str,
    session: Session,
):
    existing_user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if existing_user:
        raise AppException(
            "Username already exists",
            status_code=409,
        )

    user = User(
        username=username,
        password_hash=hash_password(password),
        role="viewer",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }
