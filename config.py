import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///shop.db")
JWT_EXPIRATION_HOURS = 24