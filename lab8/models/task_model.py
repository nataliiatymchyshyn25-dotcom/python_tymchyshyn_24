from datetime import datetime
from enum import Enum as PythonEnum
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class TaskStatus(PythonEnum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    schedule_for: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus, native_enum=False)
    )

    def __init__(
        self,
        name: str,
        description: str,
        schedule_for: datetime,
        id: UUID | None = None,
        created_at: datetime | None = None,
        status: TaskStatus = TaskStatus.TODO
    ):
        self.id = id if id is not None else uuid4()
        self.name = name
        self.description = description
        self.schedule_for = schedule_for
        self.created_at = (
            created_at if created_at is not None
            else datetime.now()
        )
        self.status = status
