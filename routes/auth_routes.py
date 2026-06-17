from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import get_db
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    phone: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    result, status_code = auth_service.register(
        db=db,
        email=data.email,
        password=data.password,
        name=data.name,
        surname=data.surname,
        phone=data.phone
    )
    return result


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result, status_code = auth_service.login(
        db=db,
        email=data.email,
        password=data.password
    )
    return result