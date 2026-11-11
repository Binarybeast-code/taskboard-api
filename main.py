from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import select

import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine) #create the tables in the database

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False 

class TaskRead(TaskCreate):
    id: int
    model_config = ConfigDict(from_attributes=True) #to read data from the database models

@app.get("/")
def root():
    return {"message": "Welcom to the Task Board API!"}

@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(models.Task)).all()

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_in: TaskCreate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_in.title
    task.description = task_in.description
    task.done = task_in.done
    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()