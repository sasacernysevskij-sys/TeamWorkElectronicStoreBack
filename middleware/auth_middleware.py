from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db
from utils.jwt_utils import decode_token


def get_current_user_id(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Токен отсутствует")

    token = authorization.split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Токен недействителен или истёк")

    return user_id