from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"messsage": "TaskBoard API is running!"}