import unittest
import subprocess
import sys
from pathlib import Path

from lab6OOP import (
    Employee,
    HourlyEmployee,
    FixedEmployee,
    FopEmployee,
    ContractEmployee,
    generate_employees,
    sort_employees,
    filter_fop,
    validate_ranges
)


class TestEmployees(unittest.TestCase):

    def test_hourly_employee(self):
        employee = HourlyEmployee(1, "Smith", 200)

        self.assertAlmostEqual(employee.calculate_salary(), 33280)
        self.assertAlmostEqual(employee.calculate_taxes(), 6489.6)

    def test_fixed_employee(self):
        employee = FixedEmployee(2, "Brown", 30000)

        self.assertAlmostEqual(employee.calculate_salary(), 30000)
        self.assertAlmostEqual(employee.calculate_taxes(), 5850)

    def test_fop_employee(self):
        employee = FopEmployee(3, "Wilson", 200, 3)

        self.assertAlmostEqual(employee.calculate_salary(), 36608)
        self.assertAlmostEqual(employee.calculate_taxes(), 3590.4)

    def test_contract_employee(self):
        employee = ContractEmployee(4, "Taylor", 10, 3000)

        self.assertAlmostEqual(employee.calculate_salary(), 30000)
        self.assertAlmostEqual(employee.calculate_taxes(), 7610)

    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            Employee(1, "Smith")


class TestEmployeeOperations(unittest.TestCase):

    def setUp(self):
        self.employees = [
            FixedEmployee(1, "Smith", 30000),
            FixedEmployee(2, "Brown", 50000),
            FixedEmployee(3, "Adams", 50000),
            FopEmployee(4, "Wilson", 200, 2),
            FopEmployee(5, "Taylor", 300, 3)
        ]

    def test_generate_employees(self):
        employees = generate_employees(20)

        self.assertEqual(len(employees), 20)
        self.assertTrue(all(isinstance(e, Employee) for e in employees))
        self.assertEqual(
            [e.employee_id for e in employees],
            list(range(1, 21))
        )

    def test_sort_employees(self):
        sort_employees(self.employees)

        surnames = [employee.surname for employee in self.employees]

        self.assertEqual(
            surnames,
            ["Taylor", "Adams", "Brown", "Wilson", "Smith"]
        )

    def test_filter_by_group(self):
        result = filter_fop(
            self.employees, 3, None, None, None, None
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].surname, "Taylor")

    def test_filter_by_income(self):
        result = filter_fop(
            self.employees, None, 40000, 60000, None, None
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].surname, "Taylor")

    def test_filter_by_taxes(self):
        result = filter_fop(
            self.employees, None, None, None, 3000, 4000
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].surname, "Wilson")

    def test_filter_no_results(self):
        result = filter_fop(
            self.employees, 4, None, None, None, None
        )

        self.assertEqual(len(result), 0)

    def test_invalid_income_range(self):
        with self.assertRaises(Exception):
            validate_ranges(50000, 20000, None, None)

    def test_invalid_tax_range(self):
        with self.assertRaises(Exception):
            validate_ranges(None, None, 5000, 2000)

    def test_valid_ranges(self):
        validate_ranges(20000, 50000, 1000, 5000)


class TestCLI(unittest.TestCase):

    def run_cli(self, *args):
        script = Path(__file__).resolve().parent.parent / "lab6OOP.py"

        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

    def test_help(self):
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("--group", result.stdout)
        self.assertIn("--min-income", result.stdout)
        self.assertIn("--max-tax", result.stdout)

    def test_count(self):
        result = self.run_cli("--count", "5")

        self.assertEqual(result.returncode, 0)

        lines = result.stdout.strip().splitlines()
        employees_count = len(lines) - 2

        self.assertEqual(employees_count, 5)

    def test_invalid_group(self):
        result = self.run_cli("--group", "5")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error", result.stderr)

    def test_invalid_income_range(self):
        result = self.run_cli(
            "--min-income", "50000",
            "--max-income", "20000"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Мінімальний дохід", result.stderr)

    def test_invalid_tax_range(self):
        result = self.run_cli(
            "--min-tax", "5000",
            "--max-tax", "2000"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Мінімальна сума податків", result.stderr)


if __name__ == "__main__":
    unittest.main()
