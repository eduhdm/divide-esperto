import unittest
from src.exceptions.exceptions import UserNotFoundException
from src.expenses.balance import Balance

class TestBalance(unittest.TestCase):

    def test_add_amount_to_user(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)

        balance.add_amount(user_id = 1, amount = 10)
        balance.add_amount(user_id = 2, amount = 50)

        self.assertTrue(balance.amount_paid_a == 110)
        self.assertTrue(balance.amount_paid_b == 50)


    def test_calculate_user_balance(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)
        self.assertTrue(balance.get_user_balance(user_id = 1) == 100)

        balance.add_amount(user_id = 2, amount = 50)
        self.assertTrue(balance.get_user_balance(user_id = 1) == 50)
        self.assertTrue(balance.get_user_balance(user_id = 2) == -50)

    def test_counterparty_balance(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)

        self.assertTrue(balance.get_user_balance(user_id = 1) == 100)
        counterparty_id = balance.get_counterparty_id(user_id = 1)

        self.assertTrue(balance.get_user_balance(user_id = counterparty_id) == -100)

    def test_add_amount_throws_when_user_not_found(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)

        with self.assertRaises(UserNotFoundException):
            balance.add_amount(user_id = 3, amount=10)

    def test_calculate_user_balance_throws_when_user_not_found(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)

        with self.assertRaises(UserNotFoundException):
            balance.get_user_balance(user_id = 3)

    def test_get_counterparty_id_throws_when_user_not_found(self):
        balance = Balance(user_a = 1, user_b = 2, amount_paid_a = 100,
                amount_paid_b = 0)

        with self.assertRaises(UserNotFoundException):
            balance.get_counterparty_id(user_id = 3)