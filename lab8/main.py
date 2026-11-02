from database.connection import Base, engine, SessionLocal
from models.task_model import Task
from models.todo_model import TodoList
from repositories.task_repository import TaskRepository
from controllers.todo_controller import TodoController
from views.todo_view import TodoView


def main():
    Base.metadata.create_all(engine)

    repository = TaskRepository(SessionLocal)
    model = TodoList(repository)
    view = TodoView()
    controller = TodoController(model, view)

    commands = {
        "1": controller.add_task,
        "2": controller.change_status,
        "3": controller.delete_task,
        "4": controller.update_task,
        "5": controller.show_tasks,
        "6": controller.filter_by_status,
        "7": controller.show_task_by_id
    }

    while True:
        choice = view.show_menu()

        if choice == "0":
            break

        action = commands.get(choice)

        if action is not None:
            action()
        else:
            view.show_message("Ви ввели неправильну команду!")


if __name__ == "__main__":
    main()
