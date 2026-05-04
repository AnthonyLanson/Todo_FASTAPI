from fastapi import FastAPI
from app.config import settings
from app.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.todos import router as todos_router

app = FastAPI(title=settings.app_name, version=settings.app_version)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to the Authenticated ToDo API"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(todos_router)