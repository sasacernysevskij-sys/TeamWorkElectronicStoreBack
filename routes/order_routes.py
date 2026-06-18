from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import get_db
from middleware.auth_middleware import get_current_user_id
from services.order_service import OrderService


router = APIRouter(prefix="/api/orders", tags=["orders"])
order_service = OrderService()


@router.post("")
def create_order(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = order_service.create_order(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("")
def get_my_orders(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = order_service.get_my_orders(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )