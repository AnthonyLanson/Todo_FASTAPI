from fastapi import FastAPI

from app.config import settings
from app.database import create_db_and_tables
from app.routers.todos import router as todos_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to the ToDo API"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

app.include_router(todos_router)