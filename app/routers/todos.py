from typing import Optional, Literal

from fastapi import APIRouter, HTTPException, Query

from app.crud import (
    create_todo,
    get_todo,
    list_todos,
    update_todo,
    patch_todo,
    delete_todo,
)
from app.database import SessionDep
from app.schemas import TodoCreate, TodoRead, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=201)
def create_todo_route(todo: TodoCreate, session: SessionDep):
    return create_todo(session, todo)


@router.get("", response_model=list[TodoRead])
def list_todos_route(
    session: SessionDep,
    completed: Optional[bool] = Query(default=None),
    priority: Optional[Literal["low", "medium", "high"]] = Query(default=None),
    sort_by: Literal["created_at", "due_date", "title"] = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="desc"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_todos(
        session=session,
        completed=completed,
        priority=priority,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo_route(todo_id: int, session: SessionDep):
    todo = get_todo(session, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_route(todo_id: int, todo: TodoCreate, session: SessionDep):
    updated = update_todo(session, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.patch("/{todo_id}", response_model=TodoRead)
def patch_todo_route(todo_id: int, todo: TodoUpdate, session: SessionDep):
    updated = patch_todo(session, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.delete("/{todo_id}")
def delete_todo_route(todo_id: int, session: SessionDep):
    deleted = delete_todo(session, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}