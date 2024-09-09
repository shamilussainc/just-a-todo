from sqlalchemy.orm import Session
from app import schemas, models


def get_task(db: Session, task_id: int):
    return db.query(models.Task).where(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.Task):
    task_in_db = models.Task(**task.model_dump())
    db.add(task_in_db)
    db.commit()
    db.refresh(task_in_db)

    return task_in_db

def update_task(
        db: Session,
        task_in_db: models.Task,
        updated_task: schemas.TaskUpdate
    ):
    task_dict = updated_task.model_dump(exclude_unset=True)
    for key, value in task_dict.items():
        setattr(task_in_db, key, value)
    db.add(task_in_db)
    db.commit()
    db.refresh(task_in_db)

    return task_in_db

def delete_task(db: Session, task: models.Task) -> bool:
    db.delete(task)
    db.commit()
