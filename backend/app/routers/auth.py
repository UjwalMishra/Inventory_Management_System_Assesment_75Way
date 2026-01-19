from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user import UserLogin, TokenResponse
from app.services.auth_service import authenticate_user
from app.schemas.user import UserSignup
from app.services.auth_service import signup_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, session: Session = Depends(get_session)):
    token = authenticate_user(data.username, data.password, session)
    return {"access_token": token}


@router.post("/signup")
def signup(
    data: UserSignup,
    session: Session = Depends(get_session),
):
    return signup_user(
        username=data.username,
        password=data.password,
        session=session,
    )