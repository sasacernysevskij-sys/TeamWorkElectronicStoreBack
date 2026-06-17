from fastapi import FastAPI

from db import init_db, engine, Base
from routes.auth_routes import router as auth_router

app = FastAPI(title="Shop API", version="1.0.0")

# Создаём таблицы при старте
Base.metadata.create_all(bind=engine)

# Подключаем роуты
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "API работает!"}