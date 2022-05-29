import unittest
from src.exceptions.exceptions import UserNotFoundException
from src.expenses.expense import Expense, ExpenseTypes

class TestExpense(unittest.TestCase):

    def test_payor_balance_is_positive_when_splitting_in_half(self):
        payor_id = 1
        user_id = 2
        expense = Expense(
            id = 1,
            expense_type=ExpenseTypes.EQUAL,
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 50)

    def test_payor_balance_is_zero_when_not_splitting(self):
        payor_id = 1
        expense = Expense(
            id = 1,
            expense_type=ExpenseTypes.EQUAL,
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 0)

    def test_payor_balance_is_total_when_buying_for_other_user(self):
        payor_id = 1
        expense = Expense(
            id = 1,
            expense_type=ExpenseTypes.EQUAL,
            description='Despesa',
            paid_by = payor_id,
            used_by = [2],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 100)

    def test_user_balance_is_negative_when_not_paying(self):
        payor_id = 1
        user_id = 2
        expense = Expense(
            id = 1,
            expense_type=ExpenseTypes.EQUAL,
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(user_id) == -50)

    def test_get_user_balance_throws_not_found(self):
        payor_id = 1
        user_id = 2
        expense = Expense(
            id = 1,
            expense_type=ExpenseTypes.EQUAL,
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        with self.assertRaises(UserNotFoundException):
            expense.get_user_balance(user_id = 3)