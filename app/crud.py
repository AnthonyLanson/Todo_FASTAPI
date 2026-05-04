from datetime import datetime
from typing import Optional, Literal
from sqlalchemy import asc, desc
from sqlmodel import select
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate
from sqlmodel import Session


def create_todo(session: Session, todo_in: TodoCreate) -> Todo:
    db_todo = Todo(**todo_in.model_dump())
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_todo(session: Session, todo_id: int) -> Optional[Todo]:
    return session.get(Todo, todo_id)


def list_todos(
    session: Session,
    completed: Optional[bool] = None,
    priority: Optional[Literal["low", "medium", "high"]] = None,
    sort_by: Literal["created_at", "due_date", "title"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    limit: int = 10,
    offset: int = 0,
) -> list[Todo]:
    statement = select(Todo)

    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    if priority is not None:
        statement = statement.where(Todo.priority == priority)

    sort_column = getattr(Todo, sort_by)
    statement = statement.order_by(desc(sort_column) if order == "desc" else asc(sort_column))
    statement = statement.offset(offset).limit(limit)

    return list(session.exec(statement).all())


def update_todo(session: Session, todo_id: int, todo_in: TodoCreate) -> Optional[Todo]:
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return None

    data = todo_in.model_dump()
    for key, value in data.items():
        setattr(db_todo, key, value)

    db_todo.updated_at = datetime.utcnow()

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def patch_todo(session: Session, todo_id: int, todo_in: TodoUpdate) -> Optional[Todo]:
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return None

    data = todo_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_todo, key, value)

    db_todo.updated_at = datetime.utcnow()
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: int) -> bool:
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True