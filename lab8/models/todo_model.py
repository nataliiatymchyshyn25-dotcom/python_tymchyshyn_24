
from uuid import UUID
from datetime import datetime

from models.task_model import Task, TaskStatus
from repositories.task_repository import TaskRepository


class TodoList:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, name, description, schedule_for):
        task = Task(
            name=name,
            description=description,
            schedule_for=schedule_for
        )
        return self.repository.add_task(task)

    def get_tasks(self):
        return self.repository.get_tasks()

    def get_task_by_id(self, task_id: UUID):
        return self.repository.get_task_by_id(task_id)

    def delete_task(self, task_id: UUID):
        return self.repository.delete_task(task_id)

    def update_task(
        self,
        task_id: UUID,
        name: str,
        description: str,
        schedule_for: datetime
    ):
        return self.repository.update_task(
            task_id, name, description, schedule_for
        )

    def change_status(self, task_id: UUID, status: TaskStatus):
        return self.repository.change_status(task_id, status)

    def filter_by_status(self, status: TaskStatus):
        return self.repository.filter_by_status(status)
