from datetime import datetime
from typing import Optional, Literal
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import Todo, User
from app.schemas import TodoCreate, TodoRead, TodoUpdate
from app.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=201)
def create_todo_route(
    todo_in: TodoCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    todo = Todo(
        **todo_in.model_dump(),
        owner_id=current_user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("", response_model=list[TodoRead])
def list_todos_route(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    completed: Optional[bool] = Query(default=None),
    priority: Optional[Literal["low", "medium", "high"]] = Query(default=None),
    sort_by: Literal["created_at", "due_date", "title"] = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="desc"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    statement = select(Todo).where(Todo.owner_id == current_user.id)

    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    if priority is not None:
        statement = statement.where(Todo.priority == priority)

    sort_column = getattr(Todo, sort_by)
    if order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    statement = statement.offset(offset).limit(limit)

    todos = session.exec(statement).all()
    return list(todos)


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo_route(
    todo_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    todo = session.get(Todo, todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_route(
    todo_id: int,
    todo_in: TodoCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    todo = session.get(Todo, todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    data = todo_in.model_dump()
    for key, value in data.items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoRead)
def patch_todo_route(
    todo_id: int,
    todo_in: TodoUpdate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    todo = session.get(Todo, todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    data = todo_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo_route(
    todo_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    todo = session.get(Todo, todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}