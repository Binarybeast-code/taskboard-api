from fastapi import FastAPI

from app import models  # noqa: F401 (loads the models so create_all sees them)
from app.config import settings
from app.database import Base, engine
from app.routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": f"Welcome to the {settings.app_name}!"}
