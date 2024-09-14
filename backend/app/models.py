from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=62), index=True)
    email = Column(String(length=320), index=True)
    hashed_password = Column(String)
    is_active = True

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    tasks = relationship(Task, back_populates="user")