from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False

class Task(TaskCreate):
    id: int

tasks : list[Task] = []
next_id = 1

@app.get("/")
def root():
    return {"massage": "Welcome to the Task Board API!"}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate):
    global next_id
    task = Task(id=next_id, **task_in.model_dump())
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks
