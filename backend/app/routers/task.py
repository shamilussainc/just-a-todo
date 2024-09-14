from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.crud import task as task_crud
from app.schemas import task as task_schemas
from app.dependencies import get_current_active_user, get_db_session
from app.models import User as UserModel


router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(get_current_active_user)])


@router.get("")
def list_tasks(
    user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)) -> list[task_schemas.Task]:
    tasks = task_crud.get_tasks(db=db, user_id=user.id)
    return tasks

@router.post("")
def create_task(
    task: task_schemas.TaskCreate,
    user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)) -> task_schemas.Task:
    task_in_db = task_crud.create_task(db=db, task=task, user_id=user.id)
    return task_in_db

@router.get("/{task_id}")
def get_task(
    task_id: int,
    user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)) -> task_schemas.Task:
    task = task_crud.get_task(db=db, task_id=task_id, user_id=user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task

@router.put("/{task_id}")
def update_task(
    task_id: int,
    updated_task: task_schemas.TaskUpdate,
    user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)) -> task_schemas.Task:
    task_in_db = task_crud.get_task(db=db, task_id=task_id, user_id=user.id)
    if not task_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task_crud.update_task(db=db, task_in_db=task_in_db, updated_task=updated_task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)):
    task = task_crud.get_task(db=db, task_id=task_id, user_id=user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    task_crud.delete_task(db=db, task=task)
