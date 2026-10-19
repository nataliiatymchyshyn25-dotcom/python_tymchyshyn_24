from abc import ABC, abstractmethod
from faker import Faker
import random
import click

fake = Faker("en_US")


class Employee(ABC):
    def __init__(self, employee_id, surname):
        self.employee_id = employee_id
        self.surname = surname

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def calculate_taxes(self) -> float:
        pass


class HourlyEmployee(Employee):
    def __init__(self, employee_id, surname, hourly_rate):
        super().__init__(employee_id, surname)
        self.hourly_rate = hourly_rate

    def calculate_salary(self) -> float:
        return 20.8 * 8 * self.hourly_rate

    def calculate_taxes(self) -> float:
        salary = self.calculate_salary()
        return salary * 0.18 + salary * 0.015


class FixedEmployee(Employee):
    def __init__(self, employee_id, surname, monthly_salary):
        super().__init__(employee_id, surname)
        self.monthly_salary = monthly_salary

    def calculate_salary(self) -> float:
        return self.monthly_salary

    def calculate_taxes(self) -> float:
        salary = self.calculate_salary()
        return salary * 0.18 + salary * 0.015


class FopEmployee(Employee):
    def __init__(self, employee_id, surname, hourly_rate, group):
        super().__init__(employee_id, surname)
        self.hourly_rate = hourly_rate
        self.group = group

    def calculate_salary(self) -> float:
        return 20.8 * 8 * self.hourly_rate * 1.10

    def calculate_taxes(self) -> float:
        salary = self.calculate_salary()
        return salary * 0.05 + 1760


class ContractEmployee(Employee):
    def __init__(self, employee_id, surname, price_per_line, lines):
        super().__init__(employee_id, surname)
        self.price_per_line = price_per_line
        self.lines = lines

    def calculate_salary(self) -> float:
        return self.price_per_line * self.lines

    def calculate_taxes(self) -> float:
        salary = self.calculate_salary()
        return salary * 0.18 + salary * 0.015 + 1760


def generate_employees(count):
    employees = []

    for i in range(count):
        employee_id = i + 1
        surname = fake.last_name()
        employee_type = random.randint(1, 4)

        if employee_type == 1:
            employee = HourlyEmployee(
                employee_id, surname, random.randint(100, 500)
            )
        elif employee_type == 2:
            employee = FixedEmployee(
                employee_id, surname, random.randint(20000, 80000)
            )
        elif employee_type == 3:
            employee = FopEmployee(
                employee_id, surname,
                random.randint(100, 500),
                random.randint(1, 4)
            )
        else:
            employee = ContractEmployee(
                employee_id, surname,
                random.randint(5, 20),
                random.randint(1000, 5000)
            )

        employees.append(employee)

    return employees


def sort_employees(employees):
    employees.sort(
        key=lambda employee: (
            -employee.calculate_salary(),
            employee.surname
        )
    )


def filter_fop(employees, group, min_income, max_income, min_tax, max_tax):
    filtered = []

    for employee in employees:
        if (
                isinstance(employee, FopEmployee)
                and (group is None or employee.group == group)
                and (min_income is None or employee.calculate_salary() >= min_income)
                and (max_income is None or employee.calculate_salary() <= max_income)
                and (min_tax is None or employee.calculate_taxes() >= min_tax)
                and (max_tax is None or employee.calculate_taxes() <= max_tax)
        ):
            filtered.append(employee)

    return filtered


def validate_ranges(min_income, max_income, min_tax, max_tax):
    if min_income is not None and max_income is not None and min_income > max_income:
        raise click.BadParameter(
            "Мінімальний дохід не може перевищувати максимальний",
        )

    if min_tax is not None and max_tax is not None and min_tax > max_tax:
        raise click.BadParameter(
            "Мінімальна сума податків не може перевищувати максимальну",
        )


def print_employees(employees, group, min_income, max_income, min_tax, max_tax, show_all):
    def print_table(workers):
        print(f"{'ID':<5} {'Прізвище':<20} {'Група':<8} {'Зарплата':>12} {'Податки':>12}")
        print("-" * 65)

        for employee in workers:
            employee_group = employee.group if isinstance(employee, FopEmployee) else "-"

            print(
                f"{employee.employee_id:<5} "
                f"{employee.surname:<20} "
                f"{str(employee_group):<8} "
                f"{employee.calculate_salary():>12.2f} "
                f"{employee.calculate_taxes():>12.2f}"
            )

        if not workers:
            print("Працівників за заданими критеріями не знайдено.")

    filters_used = any(value is not None for value in
                       [group, min_income, max_income, min_tax, max_tax])

    if filters_used:
        filtered = filter_fop(
            employees, group, min_income, max_income, min_tax, max_tax
        )

        print("Відфільтровані ФОП:")
        print_table(filtered)

    if show_all or not filters_used:
        if filters_used:
            print("\nУсі працівники:")

        print_table(employees)


@click.command()
@click.option("--group", type=click.IntRange(1, 4), help="Група ФОП")
@click.option("--min-income", type=float, help="Мінімальний дохід")
@click.option("--max-income", type=float, help="Максимальний дохід")
@click.option("--min-tax", type=float, help="Мінімальна сума податків")
@click.option("--max-tax", type=float, help="Максимальна сума податків")
@click.option("--count", default=10, type=click.IntRange(min=1), help="Згенерувати задану кількість працівників")
@click.option("--all", "show_all", is_flag=True, help="Показати всіх працівників")
def main(group, min_income, max_income, min_tax, max_tax, count, show_all):
    validate_ranges(min_income, max_income, min_tax, max_tax)

    employees = generate_employees(count)
    sort_employees(employees)

    print_employees(employees, group, min_income, max_income,min_tax, max_tax, show_all)


if __name__ == "__main__":
    main()
