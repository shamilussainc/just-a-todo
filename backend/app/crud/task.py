from sqlalchemy.orm import Session
from app.models import Task as TaskModel
from app.schemas import task as task_schema


def get_task(db: Session, task_id: int, user_id: int | None = None):
    query = db.query(TaskModel)
    if user_id:
        query = query.where(TaskModel.user_id == user_id)
    return query.where(TaskModel.id == task_id).first()


def get_tasks(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    query = db.query(TaskModel)
    if user_id:
        query = query.where(TaskModel.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def create_task(db: Session, task: task_schema.Task, user_id: int):
    task_in_db = TaskModel(**task.model_dump())
    task_in_db.user_id = user_id
    db.add(task_in_db)
    db.commit()
    db.refresh(task_in_db)

    return task_in_db

def update_task(
        db: Session,
        task_in_db: TaskModel,
        updated_task: task_schema.TaskUpdate
    ):
    task_dict = updated_task.model_dump(exclude_unset=True)
    for key, value in task_dict.items():
        setattr(task_in_db, key, value)
    db.add(task_in_db)
    db.commit()
    db.refresh(task_in_db)

    return task_in_db

def delete_task(db: Session, task: TaskModel) -> bool:
    db.delete(task)
    db.commit()
