from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from models.task_model import Task, TaskStatus


class TaskRepository:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def add_task(self, task: Task) -> Task:
        with self.session_factory.begin() as session:
            session.add(task)

        return task

    def get_tasks(self) -> list[Task]:
        with self.session_factory() as session:
            return list(
                session.scalars(select(Task)).all()
            )

    def get_task_by_id(self, task_id: UUID) -> Task | None:
        with self.session_factory() as session:
            return session.get(Task, task_id)

    def delete_task(self, task_id: UUID) -> bool:
        with self.session_factory.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                return False

            session.delete(task)
            return True

    def update_task(
        self,
        task_id: UUID,
        name: str,
        description: str,
        schedule_for: datetime
    ) -> bool:
        with self.session_factory.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                return False

            task.name = name
            task.description = description
            task.schedule_for = schedule_for

            return True

    def change_status(
        self,
        task_id: UUID,
        status: TaskStatus
    ) -> bool:
        with self.session_factory.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                return False

            task.status = status
            return True

    def filter_by_status(
        self,
        status: TaskStatus
    ) -> list[Task]:
        with self.session_factory() as session:
            return list(
                session.scalars(
                    select(Task).where(Task.status == status)
                ).all()
            )
