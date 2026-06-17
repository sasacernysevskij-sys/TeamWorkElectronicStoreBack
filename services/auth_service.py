from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session

from models.user import User
from utils.jwt_utils import create_token


class AuthService:

    def register(self, db: Session, email: str, password: str, name: str, surname: str, phone: str = ""):
        # Проверка: почта не занята
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            return {"error": "Почта уже зарегистрирована"}, 400

        # Хешируем пароль
        password_hash = generate_password_hash(password)

        # Создаём пользователя
        user = User(
            name=name,
            surname=surname,
            email=email,
            password_hash=password_hash,
            phone=phone,
            role="user",
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Создаём токен
        token = create_token(user.id)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "created_at": user.created_at.isoformat()
            }
        }, 201

    def login(self, db: Session, email: str, password: str):
        # Ищем пользователя
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return {"error": "Неверная почта или пароль"}, 401

        # Проверяем пароль
        if not check_password_hash(user.password_hash, password):
            return {"error": "Неверная почта или пароль"}, 401

        # Создаём токен
        token = create_token(user.id)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "created_at": user.created_at.isoformat()
            }
        }, 200