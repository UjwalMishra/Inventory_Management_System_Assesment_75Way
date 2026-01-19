from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import get_product_with_inventory, search_products, create_product_service
from app.core.dependencies import require_admin, get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


# create product router - ADMIN only
@router.post("/", dependencies=[Depends(require_admin)], response_model=ProductRead)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
):
    return create_product_service(data, session)


@router.get("/")
def get_products(
    session: Session = Depends(get_session),
    product_id: Optional[int] = None,
    name: Optional[str] = None,
    user=Depends(get_current_user),
):
    if product_id:
        return get_product_with_inventory(product_id, session)

    if name:
        return search_products(session, name)

    return search_products(session)