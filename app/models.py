# The table or what's stored

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    done: Mapped[bool] = mapped_column(default=False)
