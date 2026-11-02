from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from models.task_model import TaskStatus
from models.todo_model import TodoList
from views.todo_view import TodoView


@dataclass
class TodoController:
    model: TodoList
    view: TodoView

    def add_task(self):
        name, description, date = self.view.get_task_data()

        try:
            schedule_for = datetime.strptime(
                date, "%d-%m-%Y %H:%M"
            )

            if schedule_for <= datetime.now():
                "Дата виконання не може бути ранішою за дату створення завдання!"
                return

            self.model.add_task(name, description, schedule_for)
            self.view.show_message("Завдання додано!")

        except ValueError:
            self.view.show_message("Неправильний формат дати!")


    def show_tasks(self):
        tasks = self.model.get_tasks()
        self.view.show_tasks(tasks)

    def show_task_by_id(self):
        try:
            task_id = UUID(self.view.get_task_id())
        except ValueError:
            self.view.show_message("Неправильний UUID!")
            return

        task = self.model.get_task_by_id(task_id)

        if task is not None:
            self.view.show_tasks([task])
        else:
            self.view.show_message("Завдання не знайдено!")

    def delete_task(self):
        try:
            task_id = UUID(self.view.get_task_id())
        except ValueError:
            self.view.show_message("Неправильний UUID!")
            return

        if self.model.delete_task(task_id):
            self.view.show_message("Завдання видалено!")
        else:
            self.view.show_message("Завдання не знайдено!")

    def update_task(self):
        try:
            task_id = UUID(self.view.get_task_id())
        except ValueError:
            self.view.show_message("Неправильний ID!")
            return

        if self.model.get_task_by_id(task_id) is None:
            self.view.show_message("Завдання не знайдено!")
            return

        name, description, date = self.view.get_task_data()

        try:
            schedule_for = datetime.strptime(
                date, "%d-%m-%Y %H:%M"
            )
        except ValueError:
            self.view.show_message("Неправильний формат дати!")
            return

        self.model.update_task(
            task_id, name, description, schedule_for
        )

        self.view.show_message("Завдання оновлено!")

    def change_status(self):
        try:
            task_id = UUID(self.view.get_task_id())
        except ValueError:
            self.view.show_message("Неправильний ID!")
            return

        choice = self.view.get_status()

        statuses = {
            "1": TaskStatus.TODO,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.DONE
        }

        if choice not in statuses:
            self.view.show_message("Неправильний статус!")
            return

        if self.model.change_status(task_id, statuses[choice]):
            self.view.show_message("Статус змінено!")
        else:
            self.view.show_message("Завдання не знайдено!")

    def filter_by_status(self):
        choice = self.view.get_status()

        statuses = {
            "1": TaskStatus.TODO,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.DONE
        }

        if choice not in statuses:
            self.view.show_message("Неправильний статус!")
            return

        tasks = self.model.filter_by_status(statuses[choice])
        self.view.show_tasks(tasks)