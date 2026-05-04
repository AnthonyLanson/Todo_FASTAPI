from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False, index=True)
    priority: str = Field(default="medium", index=True)
    due_date: Optional[date] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)