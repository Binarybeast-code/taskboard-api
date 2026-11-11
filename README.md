# TaskBoard API

A task manager API built with FastAPI, built phase by phase for learning.

## Phase 1: CRUD in memory
- POST /tasks creates a task (201)
- GET /tasks lists tasks, GET /tasks/{id} gets one (404 if missing)
- PUT /tasks/{id} updates, DELETE /tasks/{id} removes (204)

## What I learned
- Input model (TaskCreate) vs output model (Task)
- raise HTTPException for errors, return for success
- PUT is idempotent, POST is not

## Run it
pip install -r requirements.txt
fastapi dev main.py
