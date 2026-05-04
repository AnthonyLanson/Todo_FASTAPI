from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = False
    priority: str = Field(default="medium")
    due_date: Optional[date] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None)
    due_date: Optional[date] = None

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime