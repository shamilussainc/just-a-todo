from typing import Annotated
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.models import Task as TaskModel, Base
from .database import SessionLocal, engine, get_db_session


app = FastAPI()


@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db_session)) -> list[schemas.Task]:
    tasks = crud.get_tasks(db=db)
    return tasks

@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db_session)) -> schemas.Task:
    task = crud.create_task(db=db, task=task)
    return task

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db_session)) -> schemas.Task:
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db_session)) -> schemas.Task:
    task_in_db = crud.get_task(db=db, task_id=task_id) 
    if not task_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return crud.update_task(db=db, task_in_db=task_in_db, updated_task=updated_task)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db_session)):
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    crud.delete_task(db=db, task=task)
