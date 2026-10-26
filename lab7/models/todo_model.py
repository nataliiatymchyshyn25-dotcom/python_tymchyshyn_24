from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from models.task_model import Task, TaskStatus


@dataclass
class TodoList:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, name, description, schedule_for):
        task = Task(
            name=name,
            description=description,
            schedule_for=schedule_for
        )
        self.tasks.append(task)
        return task

    def get_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id: UUID):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def delete_task(self, task_id: UUID):
        task = self.get_task_by_id(task_id)

        if task is not None:
            self.tasks.remove(task)
            return True

        return False

    def update_task(self, task_id: UUID, name: str,
                    description: str, schedule_for: datetime):
        task = self.get_task_by_id(task_id)

        if task is not None:
            task.name = name
            task.description = description
            task.schedule_for = schedule_for
            return True

        return False

    def change_status(self, task_id: UUID, status: TaskStatus):
        task = self.get_task_by_id(task_id)

        if task is not None:
            task.status = status
            return True

        return False

    def filter_by_status(self, status: TaskStatus):
        result = []

        for task in self.tasks:
            if task.status == status:
                result.append(task)

        return result