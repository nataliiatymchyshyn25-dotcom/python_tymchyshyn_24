from models.todo_model import TodoList
from views.todo_view import TodoView
from controllers.todo_controller import TodoController


def main():
    model = TodoList()
    view = TodoView()
    controller = TodoController(model, view)

    while True:
        choice = view.show_menu()

        match choice:
            case "1":
                controller.add_task()
            case "2":
                controller.change_status()
            case "3":
                controller.delete_task()
            case "4":
                controller.update_task()
            case "5":
                controller.show_tasks()
            case "6":
                controller.filter_by_status()
            case "7":
                controller.show_task_by_id()
            case "0":
                break
            case _:
                view.show_message("Ви ввели неправильну команду!")


if __name__ == "__main__":
    main()