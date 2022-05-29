import unittest
from src.exceptions.exceptions import UserNotFoundException
from src.cli.app import ShellController

from src.expenses.expense import Expense, ExpenseBase, ExpenseEqual, ExpensePercentage, ExpenseTypes, ExpenseValue

class TestInteractiveShell(unittest.TestCase):

    def setUp(self):
        self.controller = ShellController()

    def test_add_user_to_group(self):
        self.controller.add_user(user_name = "Eduardo")
        self.assertTrue(len(self.controller.group.user_dict.keys()) == 1)

        self.controller.add_user(user_name = "Lucas")
        self.assertTrue(len(self.controller.group.user_dict.keys()) == 2)

    def test_create_equal_expense(self):
        self.controller.add_user(user_name = "Eduardo")
        self.controller.add_user(user_name = "Lucas")

        expense = self.controller.create_exp(
            exp_type='equal',
            total_value=100,
            description='test',
            paid_by=1,
            used_by=[1, 2],
        )

        self.assertTrue(type(self.controller.group.expenses[0].get_expense()) is ExpenseEqual)

    def test_create_percentage_expense(self):
        self.controller.add_user(user_name = "Eduardo")
        self.controller.add_user(user_name = "Lucas")

        expense = self.controller.create_exp(
            exp_type='percentage',
            total_value=100,
            description='test',
            paid_by=1,
            used_by=[1, 2],
            percentage_used=[20, 80],
        )

        self.assertTrue(type(self.controller.group.expenses[0].get_expense()) is
                ExpensePercentage)

    def test_create_value_expense(self):
        self.controller.add_user(user_name = "Eduardo")
        self.controller.add_user(user_name = "Lucas")

        expense = self.controller.create_exp(
            exp_type='value',
            total_value=100,
            description='test',
            paid_by=1,
            used_by=[1, 2],
            value_used=[20, 80],
        )

        self.assertTrue(type(self.controller.group.expenses[0].get_expense()) is
                ExpenseValue)

    def test_throws_on_invalid_expense_type(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='invalid',
                total_value=100,
                description='test',
                paid_by=1,
                used_by=[1, 2],
                value_used=[20, 80],
            )

    def test_throws_on_invalid_expense_total_value(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='equal',
                total_value=-100,
                description='test',
                paid_by=1,
                used_by=[1, 2],
            )

    def test_throws_on_empty_expense_used_by(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='equal',
                total_value=-100,
                description='test',
                paid_by=1,
                used_by=[],
            )

    def test_throws_on_invalid_expense_description(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='equal',
                total_value=-100,
                description=5,
                paid_by=1,
                used_by=[1, 2],
            )

    def test_throws_on_invalid_expense_params_length(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='percentage',
                total_value=-100,
                description=5,
                paid_by=1,
                used_by=[1, 2],
                percentage_used=[70, 20, 10]
            )

    def test_throws_on_invalid_percentage_total(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='percentage',
                total_value=-100,
                description=5,
                paid_by=1,
                used_by=[1, 2],
                percentage_used=[70, 0, 0]
            )

    def test_throws_on_invalid_value_total(self):
        with self.assertRaises(Exception):
            self.controller.create_exp(
                exp_type='value',
                total_value=-100,
                description=5,
                paid_by=1,
                used_by=[1, 2],
                value_used=[70, 0, 0]
            )

    def test_throws_on_invalid_users(self):
        with self.assertRaises(Exception):
            self.controller.print_user_balance_report(user_id = 999)
