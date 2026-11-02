
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from database.connection import Base
from models.task_model import Task, TaskStatus
from repositories.task_repository import TaskRepository
from models.todo_model import TodoList
from controllers.todo_controller import TodoController
from views.todo_view import TodoView
from main import main


TEST_DATABASE_URL = "postgresql+psycopg://test_user:password@localhost:5443/test_db"


class TestTaskRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)

        cls.SessionTest = sessionmaker(
            bind=cls.engine,
            expire_on_commit=False
        )

    def setUp(self):
        with self.SessionTest.begin() as session:
            session.execute(delete(Task))

        self.repository = TaskRepository(self.SessionTest)
        self.model = TodoList(self.repository)
        self.date = datetime.now() + timedelta(days=5)

    def test_add_and_get_task(self):
        task = self.model.add_task("Python", "Lab8", self.date)

        found = self.repository.get_task_by_id(task.id)

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Python")
        self.assertEqual(found.status, TaskStatus.TODO)

    def test_get_all_tasks(self):
        self.model.add_task("Python", "Lab8", self.date)
        self.model.add_task("Java", "Lab8", self.date)

        tasks = self.repository.get_tasks()

        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        task = self.model.add_task("Python", "Old description", self.date)

        new_date = self.date + timedelta(days=2)

        result = self.repository.update_task( task.id, "Java", "New description", new_date)

        updated = self.repository.get_task_by_id(task.id)

        self.assertTrue(result)
        self.assertEqual(updated.name, "Java")
        self.assertEqual(updated.description, "New description")
        self.assertEqual(updated.schedule_for, new_date)

    def test_change_status(self):
        task = self.model.add_task("Python", "Lab8", self.date)

        result = self.repository.change_status(
            task.id, TaskStatus.DONE
        )

        updated = self.repository.get_task_by_id(task.id)

        self.assertTrue(result)
        self.assertEqual(updated.status, TaskStatus.DONE)

    def test_filter_by_status(self):
        first = self.model.add_task( "Python", "Lab8", self.date)
        self.model.add_task("Java", "Lab8", self.date)

        self.repository.change_status(first.id, TaskStatus.DONE)

        tasks = self.repository.filter_by_status(TaskStatus.DONE)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, first.id)

    def test_delete_task(self):
        task = self.model.add_task("Python", "Lab8", self.date)

        self.assertTrue(
            self.repository.delete_task(task.id)
        )
        self.assertIsNone(
            self.repository.get_task_by_id(task.id)
        )

    def test_nonexistent_task(self):
        unknown_id = uuid4()

        self.assertIsNone(
            self.repository.get_task_by_id(unknown_id)
        )
        self.assertFalse(
            self.repository.delete_task(unknown_id)
        )
        self.assertFalse(
            self.repository.change_status(
                unknown_id, TaskStatus.DONE
            )
        )
        self.assertFalse(
            self.repository.update_task(
                unknown_id, "Name", "Description", self.date
            )
        )

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

if __name__ == "__main__":
    unittest.main()
