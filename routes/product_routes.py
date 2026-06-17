from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from db import get_db
from models.user import User
from middleware.auth_middleware import get_current_user, get_current_admin_user
from services.product_service import ProductService


router = APIRouter(prefix="/api/products", tags=["products"])
product_service = ProductService()


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    article: str = Field(min_length=1, max_length=10)
    description: str | None = None
    price: float
    product_type: str = Field(min_length=1, max_length=30)
    stock: int = 0
    rating: float = 0.0
    image_url: str | None = None


@router.get("")
def get_products(
    product_type: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    result, status_code = product_service.get_products(
        db=db,
        product_type=product_type,
        skip=skip,
        limit=limit
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.post("")
def create_product(
    data: ProductCreateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    result, status_code = product_service.create_product(
        db=db,
        name=data.name,
        article=data.article,
        description=data.description,
        price=data.price,
        product_type=data.product_type,
        stock=data.stock,
        rating=data.rating,
        image_url=data.image_url
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )