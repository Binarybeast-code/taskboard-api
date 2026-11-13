# Here is what travels over the API
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False


class TaskRead(TaskCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
