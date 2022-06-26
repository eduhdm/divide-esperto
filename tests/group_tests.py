import unittest
from dividexp.expenses.expense import ExpenseTypes

from dividexp.expenses.group import Group, SplitCalc

class TestGorups(unittest.TestCase):

    def test_add_new_user_to_group(self):
        group = Group()
        user_id = group.add_user('username')
        self.assertEquals(user_id, 1)
    
    def test_add_multiple_users_to_group(self):
        group = Group()
        group.add_user('username_a')        
        user_id = group.add_user('username_b')
        self.assertEquals(user_id, 2)

    def test_group_with_equal_expense(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.EQUAL,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            total_value=100,
            description='Expense'
        )

        usera_report = group.get_user_balance_report(usera_id)
        userb_report = group.get_user_balance_report(userb_id)

        self.assertIn('You owe 50.0', userb_report)
        self.assertIn('You owe a total of 50.0 to username_a', userb_report)
        self.assertIn('You are owed 50.0', usera_report)
        self.assertIn('username_b owes you a total of 50.0', usera_report)

    def test_group_with_percentage_expense(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.PERCENTAGE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            percentage_used=[40, 60],
            total_value=100,
            description='Expense'
        )

        usera_report = group.get_user_balance_report(usera_id)
        userb_report = group.get_user_balance_report(userb_id)

        self.assertIn('You owe 60.0', userb_report)
        self.assertIn('You owe a total of 60.0 to username_a', userb_report)
        self.assertIn('You are owed 60.0', usera_report)
        self.assertIn('username_b owes you a total of 60.0', usera_report)

    def test_group_with_value_expense(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.VALUE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            value_used=[35, 65],
            total_value=100,
            description='Expense'
        )

    def test_group_with_multiple_expenses(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.VALUE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            value_used=[35, 65],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.PERCENTAGE,
            paid_by=userb_id,
            used_by=[usera_id, userb_id],
            percentage_used=[40, 60],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.EQUAL,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            total_value=100,
            description='Expense'
        )

        usera_report = group.get_user_balance_report(usera_id)
        userb_report = group.get_user_balance_report(userb_id)

        self.assertIn('You owe 75.0',userb_report)
        self.assertIn('You owe a total of 75.0 to username_a', userb_report)
        self.assertIn('You are owed 75.0',  usera_report)
        self.assertIn('username_b owes you a total of 75.0',  usera_report)
    
    def test_group_with_multiple_expenses_that_cancel_out(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.VALUE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            value_used=[35, 65],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.PERCENTAGE,
            paid_by=userb_id,
            used_by=[usera_id, userb_id],
            percentage_used=[80, 20],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.PERCENTAGE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            percentage_used=[85, 15],
            total_value=100,
            description='Expense'
        )

        self.assertIn('You are all set', group.get_user_balance_report(userb_id))
        self.assertIn('You are all set', group.get_user_balance_report(usera_id))

    def test_group_with_invalid_expense(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        
        with self.assertRaises(Exception):
            group.add_expense(
                expense_type=ExpenseTypes.PERCENTAGE,
                paid_by=usera_id,
                used_by=[usera_id, userb_id],
                percentage_used=[40, 50],
                total_value=100,
                description='Expense'
            )

    def test_get_report_for_invalid_user(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        group.add_expense(
            expense_type=ExpenseTypes.EQUAL,
            paid_by=usera_id,
            used_by=[usera_id, userb_id],
            total_value=100,
            description='Expense'
        )
        with self.assertRaises(Exception):
            group.get_user_balance_report(userb_id + 1)
    
    def test_group_with_multiple_users_calculates_all_expenses(self):
        group = Group()
        usera_id = group.add_user('username_a')
        userb_id = group.add_user('username_b')
        userc_id = group.add_user('username_c')
        group.add_expense(
            expense_type=ExpenseTypes.VALUE,
            paid_by=usera_id,
            used_by=[usera_id, userb_id, userc_id],
            value_used=[35, 40, 25],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.PERCENTAGE,
            paid_by=userb_id,
            used_by=[usera_id, userb_id, userc_id],
            percentage_used=[25, 40, 35],
            total_value=100,
            description='Expense'
        )
        group.add_expense(
            expense_type=ExpenseTypes.EQUAL,
            paid_by=userc_id,
            used_by=[usera_id, userb_id, userc_id],
            total_value=150,
            description='Expense'
        )
        usera_report = group.get_user_balance_report(usera_id)
        userb_report = group.get_user_balance_report(userb_id)
        userc_report = group.get_user_balance_report(userc_id)

        self.assertIn('You owe 10.0', usera_report)
        self.assertIn('username_b owes you a total of 15.0', usera_report)
        self.assertIn('You owe a total of 25.0 to username_c', usera_report)
        self.assertIn('You owe 30.0', userb_report)
        self.assertIn('You owe a total of 15.0 to username_a', userb_report)
        self.assertIn('You owe a total of 15.0 to username_c', userb_report)
        self.assertIn('You are owed 40.0', userc_report)
        self.assertIn('username_a owes you a total of 25.0', userc_report)
        self.assertIn('username_b owes you a total of 15.0', userc_report)




