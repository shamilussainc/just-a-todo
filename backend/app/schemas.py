from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
