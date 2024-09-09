from datetime import datetime
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    is_done: bool = False

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_done: bool = False


    class Config:
        from_attributes = True
