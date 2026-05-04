import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ToDo API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

settings = Settings()