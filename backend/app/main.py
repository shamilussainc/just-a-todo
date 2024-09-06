from fastapi import FastAPI
from .schemas import Task


app = FastAPI()


@app.get("/tasks")
def list_tasks():
    import datetime
    task1 = Task(title="task 1", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
    return [task1 for _ in range(5)]


@app.post("/tasks")
def create_task():
    return "task1"


@app.get("/tasks/{task_id}")
def get_task():
    return "task1"


@app.put("/tasks/{task_id}")
def update_task():
    return "task1"
