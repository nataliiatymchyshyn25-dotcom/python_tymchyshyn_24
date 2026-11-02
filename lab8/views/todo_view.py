class TodoView:

    def show_menu(self):
        print("\n===== TO-DO LIST =====")
        print("1. Додати завдання")
        print("2. Змінити статус")
        print("3. Видалити завдання")
        print("4. Редагувати завдання")
        print("5. Показати всі завдання")
        print("6. Фільтрувати за статусом")
        print("7. Знайти завдання за ID")
        print("0. Вихід")

        return input("Оберіть дію: ")

    def show_message(self, message):
        print(message)

    def get_task_data(self):
        name = input("Назва: ")
        description = input("Опис: ")
        schedule_for = input("Дата та час виконання (DD-MM-YYYY HH:MM): ")

        return name, description, schedule_for

    def get_task_id(self):
        return input("Введіть ID завдання: ")

    def get_status(self):
        print("1. ToDo")
        print("2. InProgress")
        print("3. Done")

        return input("Оберіть статус: ")

    def show_tasks(self, tasks):
        if not tasks:
            print("Завдань не знайдено.")
            return

        headers = (
            f"{'ID':36} | {'Name':15} | {'Description':20} | "
            f"{'Created at':19} | {'Scheduled for':19} | {'Status':12}"
        )

        print(headers)
        print("-" * len(headers))

        for task in tasks:
            print(
                f"{str(task.id):36} | "
                f"{task.name[:15]:15} | "
                f"{task.description[:20]:20} | "
                f"{task.created_at:%d-%m-%Y %H:%M:%S} | "
                f"{task.schedule_for:%d-%m-%Y %H:%M:%S} | "
                f"{task.status.value:12}"
            )