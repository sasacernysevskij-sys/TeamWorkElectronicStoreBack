from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.user import User
from utils.jwt_utils import create_token

class AuthService:

    def register(self, email, password, name, surname, phone=""):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Почта уже зарегистрирована"}, 400

        password_hash = generate_password_hash(password)

        user = User(
            name=name,
            surname=surname,
            email=email,
            password_hash=password_hash,
            phone=phone,
            role="user",
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()

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

    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "Неверная почта или пароль"}, 401

        if not check_password_hash(user.password_hash, password):
            return {"error": "Неверная почта или пароль"}, 401

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