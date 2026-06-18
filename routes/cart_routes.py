from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from db import get_db
from middleware.auth_middleware import get_current_user_id
from services.cart_service import CartService


router = APIRouter(prefix="/api/cart", tags=["cart"])
cart_service = CartService()


class CartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


@router.post("/items")
def add_to_cart(
    data: CartItemRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = cart_service.add_to_cart(
        db=db,
        user_id=current_user_id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("")
def get_cart(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = cart_service.get_cart(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.delete("")
def clear_cart(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = cart_service.clear_cart(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )