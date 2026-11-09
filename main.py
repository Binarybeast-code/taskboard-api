from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):  #describes what the client
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

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_in: TaskCreate):
    for task in tasks:
        if task.id == task_id:
            task.title = task_in.title
            task.description = task_in.description
            task.done = task_in.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")
