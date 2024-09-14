from fastapi import FastAPI
from app.routers import task_router, user_router

app = FastAPI()


@app.get("/")
def root():
    return {
        "detail": "Wellcome home amigo!"
    }


app.include_router(router=task_router)
app.include_router(router=user_router)
