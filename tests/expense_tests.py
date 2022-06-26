import unittest
from dividexp.exceptions.exceptions import UserNotFoundException
from dividexp.expenses.expense import Expense, ExpenseBase, ExpenseEqual, ExpensePercentage, ExpenseTypes, ExpenseValue


class TestExpense(unittest.TestCase):
    def test_initialize_expense_equal(self):
        expense = Expense(
            id=1,
            description='Despesa',
            expense_type=ExpenseTypes.EQUAL,
            paid_by = 1,
            used_by = [1],
            total_value = 100)

        self.assertTrue(type(expense.get_expense()) is ExpenseEqual)

    def test_initialize_expense_value(self):
        expense = Expense(
            id=1,
            paid_by=1,
            expense_type=ExpenseTypes.VALUE,
            description='Despesa',
            used_by=[1, 2],
            value_used=[20, 80],
            total_value=100)

        self.assertTrue(type(expense.get_expense()) is ExpenseValue)

    def test_initialize_expense_percentage(self):
        expense = Expense(
            id=1,
            paid_by=1,
            expense_type=ExpenseTypes.PERCENTAGE,
            description='Despesa',
            used_by=[1, 2, 3],
            percentage_used=[20, 40, 40],
            total_value=100)

        self.assertTrue(type(expense.get_expense()) is ExpensePercentage)

    def test_throw_on_invalid_exception_type(self):
        with self.assertRaises(Exception) as error:
            Expense(id=1, expense_type=999)
            self.assertEqual(
                'Invalid Expense type.',
                str(error.exception)
            )


class TestExpenseBase(unittest.TestCase):
    def test_throw_exception_negative_total_value(self):
        with self.assertRaises(Exception) as error:
            ExpenseBase(total_value=-1)
            self.assertEqual(
                'Expense value cannot be negative or zero.',
                str(error.exception)
            )

    def test_throw_exception_zero_total_value(self):
        with self.assertRaises(Exception) as error:
            ExpenseBase(total_value=0)
            self.assertEqual(
                'Expense value cannot be negative or zero.',
                str(error.exception)
            )

    def test_throw_exception_empty_used_by(self):
        with self.assertRaises(Exception) as error:
            ExpenseBase(total_value=20, used_by=[])
            self.assertEqual(
                'Used by cannot be empty.',
                str(error.exception)
            )

    def test_throw_exception_invalid_description(self):
        with self.assertRaises(Exception) as error:
            ExpenseBase(total_value=20, used_by=[1], description='')
            self.assertEqual(
                'Description must be a valid string.',
                str(error.exception)
            )

    def test_throw_not_implemented_get_user_balance(self):
        with self.assertRaises(Exception) as error:
            expense = ExpenseBase(
                description='Despesa',
                paid_by = 1,
                used_by = [1, 2],
                total_value = 100)
            expense.get_user_balance(1)

            self.assertEqual(
                'Not implemented',
                str(error.exception)
            )

class TestExpenseEqual(unittest.TestCase):

    def test_payor_balance_is_positive_when_splitting_in_half(self):
        payor_id = 1
        user_id = 2
        expense = ExpenseEqual(
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 50)

    def test_payor_balance_is_zero_when_not_splitting(self):
        payor_id = 1
        expense = ExpenseEqual(
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 0)

    def test_payor_balance_is_total_when_buying_for_other_user(self):
        payor_id = 1
        expense = ExpenseEqual(
            description='Despesa',
            paid_by = payor_id,
            used_by = [2],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(payor_id) == 100)

    def test_user_balance_is_negative_when_not_paying(self):
        payor_id = 1
        user_id = 2
        expense = ExpenseEqual(
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        self.assertTrue(expense.get_user_balance(user_id) == -50)

    def test_get_user_balance_throws_not_found(self):
        payor_id = 1
        user_id = 2
        expense = ExpenseEqual(
            description='Despesa',
            paid_by = payor_id,
            used_by = [payor_id, user_id],
            total_value = 100)

        with self.assertRaises(UserNotFoundException):
            expense.get_user_balance(user_id = 3)

class TestExpensePercentage(unittest.TestCase):
    def test_throw_exception_invalid_used_by_and_percentage(self):
        with self.assertRaises(Exception) as error:
            ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                percentage_used=[20, 30, 50],
                total_value=100)

            self.assertEqual(
                'Used list and percentage list must have the same length.',
                str(error.exception)
            )

    def test_throw_exception_percentage_total_not_100(self):
        with self.assertRaises(Exception) as error:
            ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                percentage_used=[20, 30],
                total_value=100)

            self.assertEqual(
                'Percentage total should be equal a 100.',
                str(error.exception)
            )

    def test_throw_user_not_found_exception_on_user_balance(self):
        expense = ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                percentage_used=[70, 30],
                total_value=100)
        with self.assertRaises(UserNotFoundException) as error:
            expense.get_user_balance(3)

    def test_get_balance_paid_by_and_not_used_is_total(self):
        total_value = 100
        expense = ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[2, 3],
                percentage_used=[40, 60],
                total_value=total_value)

        self.assertEquals(expense.get_user_balance(1), total_value)

    def test_get_user_balance_when_user_paid_and_used_is_correct(self):
        expense = ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2, 3],
                percentage_used=[20, 40, 40],
                total_value=100)

        self.assertEquals(expense.get_user_balance(1), 80) # total_value - 20 = 80

    def test_get_user_balance_when_user_just_used_is_correct(self):
        expense = ExpensePercentage(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2, 3],
                percentage_used=[30, 40, 30],
                total_value=300)

        self.assertEquals(expense.get_user_balance(2), -120) # - 40% of 300
        self.assertEquals(expense.get_user_balance(3), -90) # - 30% of 300

class TestExpenseValue(unittest.TestCase):
    def test_throw_exception_invalid_used_by_and_used_value(self):
        with self.assertRaises(Exception) as error:
            ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                value_used=[20, 30, 50],
                total_value=100)

            self.assertEqual(
                'Used list and value list must have the same length.',
                str(error.exception)
            )

    def test_throw_exception_value_used_sum_is_not_total_value(self):
        with self.assertRaises(Exception) as error:
            ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                value_used=[20, 30],
                total_value=100)

            self.assertEqual(
                'Sum of used value must be equal total value.',
                str(error.exception)
            )

    def test_throw_user_not_found_exception_on_user_balance(self):
        expense = ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2],
                value_used=[20, 80],
                total_value=100)
        with self.assertRaises(UserNotFoundException) as error:
            expense.get_user_balance(3)

    def test_get_balance_paid_by_and_not_used_is_total(self):
        total_value = 100
        expense = ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[2, 3],
                value_used=[40, 60],
                total_value=total_value)

        self.assertEquals(expense.get_user_balance(1), total_value)

    def test_get_user_balance_when_user_paid_and_used_is_correct(self):
        expense = ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2, 3],
                value_used=[40, 80, 70],
                total_value=190)

        self.assertEquals(expense.get_user_balance(1), 150) # 190 - 40 = 150

    def test_get_user_balance_when_user_just_used_is_correct(self):
        expense = ExpenseValue(
                paid_by=1,
                description='Despesa',
                used_by=[1, 2, 3],
                value_used=[40, 80, 70],
                total_value=190)

        self.assertEquals(expense.get_user_balance(2), -80) # - used_value
        self.assertEquals(expense.get_user_balance(3), -70) # - used_value

