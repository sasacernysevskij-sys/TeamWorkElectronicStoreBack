from fastapi import FastAPI

from db import init_db, engine, Base
from models.user import User
from models.product import Product

from routes.auth_routes import router as auth_router
from routes.product_routes import router as product_router

app = FastAPI(title="Shop API", version="1.0.0")

# Создаём таблицы при старте
Base.metadata.create_all(bind=engine)

# Подключаем роуты
app.include_router(auth_router)
app.include_router(product_router)


@app.get("/")
def home():
    return {"message": "API работает!"}