import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from models.task_model import TaskStatus
from models.todo_model import TodoList
from controllers.todo_controller import TodoController
from views.todo_view import TodoView
from main import main


class TestTodo(unittest.TestCase):

    def setUp(self):
        self.model = TodoList()
        self.view = Mock()
        self.controller = TodoController(self.model, self.view)
        self.date = datetime.now() + timedelta(days=5)
        self.task = self.model.add_task("Python", "MVC", self.date)

    def test_create_task(self):
        self.assertEqual(len(self.model.get_tasks()), 1)
        self.assertIsInstance(self.task.id, UUID)
        self.assertEqual(self.task.status, TaskStatus.TODO)

    def test_find_task(self):
        self.assertEqual(self.model.get_task_by_id(self.task.id), self.task)
        self.assertIsNone(self.model.get_task_by_id(uuid4()))

    def test_delete_task(self):
        self.assertTrue(self.model.delete_task(self.task.id))
        self.assertFalse(self.model.delete_task(uuid4()))
        self.assertEqual(self.model.get_tasks(), [])

    def test_update_task(self):
        self.assertTrue(self.model.update_task(
            self.task.id, "Java", "New", self.date
        ))
        self.assertEqual(self.task.name, "Java")
        self.assertFalse(self.model.update_task(
            uuid4(), "Java", "New", self.date
        ))

    def test_status_and_filter(self):
        self.model.change_status(self.task.id, TaskStatus.DONE)
        self.assertEqual(self.task.status, TaskStatus.DONE)
        self.assertEqual(
            self.model.filter_by_status(TaskStatus.DONE), [self.task]
        )
        self.assertEqual(
            self.model.filter_by_status(TaskStatus.TODO), []
        )

    def test_add_task_controller(self):
        date = datetime.now() + timedelta(days=10)
        self.view.get_task_data.return_value = (
            "SQL", "Database", date.strftime("%d-%m-%Y %H:%M")
        )
        self.controller.add_task()
        self.assertEqual(len(self.model.tasks), 2)

    def test_invalid_date(self):
        for date in ["wrong", "01-01-2020 10:00"]:
            self.view.get_task_data.return_value = ("SQL", "Test", date)
            self.controller.add_task()
        self.assertEqual(len(self.model.tasks), 1)

    def test_controller_actions(self):
        self.view.get_task_id.return_value = str(self.task.id)
        self.view.get_status.return_value = "3"

        self.controller.change_status()
        self.assertEqual(self.task.status, TaskStatus.DONE)

        self.controller.show_task_by_id()
        self.view.show_tasks.assert_called_with([self.task])

        self.controller.delete_task()
        self.assertEqual(self.model.tasks, [])

    def test_controller_filter(self):
        self.view.get_status.return_value = "1"
        self.controller.filter_by_status()
        self.view.show_tasks.assert_called_with([self.task])

    @patch("builtins.input", side_effect=[
        "Python", "MVC", "01-12-2026 15:00"
    ])
    def test_view_input(self, mock_input):
        self.assertEqual(
            TodoView().get_task_data(),
            ("Python", "MVC", "01-12-2026 15:00")
        )

    @patch("builtins.print")
    def test_view_table(self, mock_print):
        view = TodoView()
        view.show_tasks([self.task])
        view.show_tasks([])
        self.assertTrue(mock_print.called)

    @patch("main.TodoController")
    @patch("main.TodoView")
    def test_main_menu(self, mock_view, mock_controller):
        mock_view.return_value.show_menu.side_effect = [
            "1", "2", "3", "4", "5", "6", "7", "9", "0"
        ]

        main()

        controller = mock_controller.return_value
        controller.add_task.assert_called_once()
        controller.delete_task.assert_called_once()
        controller.update_task.assert_called_once()
        controller.show_tasks.assert_called_once()
        controller.change_status.assert_called_once()
        controller.filter_by_status.assert_called_once()
        controller.show_task_by_id.assert_called_once()

    def test_controller_update(self):
        self.view.get_task_id.return_value = str(self.task.id)
        date = datetime.now() + timedelta(days=7)

        self.view.get_task_data.return_value = (
            "Java", "Новий опис", date.strftime("%d-%m-%Y %H:%M")
        )

        self.controller.update_task()

        self.assertEqual(self.task.name, "Java")
        self.assertEqual(self.task.description, "Новий опис")

    def test_controller_update_wrong_id(self):
        self.view.get_task_id.return_value = "wrong"

        self.controller.update_task()

        self.view.show_message.assert_called_with("Неправильний ID!")

    def test_controller_update_wrong_date(self):
        self.view.get_task_id.return_value = str(self.task.id)
        self.view.get_task_data.return_value = (
            "Java", "Новий опис", "wrong"
        )

        self.controller.update_task()

        self.assertEqual(self.task.name, "Python")

    def test_controller_status_wrong_choice(self):
        self.view.get_task_id.return_value = str(self.task.id)
        self.view.get_status.return_value = "9"

        self.controller.change_status()

        self.assertEqual(self.task.status, TaskStatus.TODO)
        self.view.show_message.assert_called_with("Неправильний статус!")

    def test_controller_task_not_found(self):
        self.view.get_task_id.return_value = str(uuid4())

        self.controller.show_task_by_id()

        self.view.show_message.assert_called_with("Завдання не знайдено!")


if __name__ == "__main__":
    unittest.main()