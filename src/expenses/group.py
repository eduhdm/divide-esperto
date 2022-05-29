from enum import Enum
from typing import Dict, List
from exceptions.exceptions import UserNotFoundException
from expenses.balance import Balance
from expenses.expense import Expense
from expenses.user import User

class SplitCalc(Enum):
  DEFAULT = 1 # Show all values that a user owes to others
  SIMPLIFIED = 2 # Simplify debts by transferring values that gives


class Group:
  expenses: List[Expense] = []
  user_dict: Dict[int, User] = dict()
  balance_users: List[Balance] = []
  split_calc_type: SplitCalc

  def __init__(self, split_calc_type: SplitCalc = SplitCalc.DEFAULT):
    self.expenses = []
    self.users = []
    self.split_calc_type = split_calc_type

  def _get_balance_index(self, user_id_a, user_id_b):
    def is_users_balance(b: Balance):
      b_users = [b.user_a, b.user_b]
      return user_id_a in b_users and user_id_b in b_users

    try:
      balance = [b for b in self.balance_users if is_users_balance(b)][0]
      return self.balance_users.index(balance)
    except IndexError:
      return -1

  def _upsert_balance(self, user_a: int, user_b: int, amount_paid_by_a: float):
    index = self._get_balance_index(user_a, user_b)
    if (index > -1):
      self.balance_users[index].add_amount(user_a, amount_paid_by_a)
    else:
      self.balance_users.append(Balance(user_a, user_b, amount_paid_by_a, 0))


  def add_user(self, user_name: str) -> int:
    user_id = len(self.user_dict.keys()) + 1
    user = User(user_id, user_name)
    self.user_dict[user_id] = user

    return user_id

  def add_expense(self, **kwargs) -> int:
    expense_id = len(self.expenses) + 1
    expense = Expense(expense_id, **kwargs)
    self.expenses.append(expense)

    paid_by_id = expense.paid_by
    self.user_dict[paid_by_id].add_balance(expense.get_user_balance(paid_by_id))
    for user_id in self.user_dict.keys():
      if (user_id == paid_by_id):
        continue

      value_owed = expense.get_user_balance(user_id)
      self.user_dict[user_id].add_balance(value_owed)
      self._upsert_balance(expense.paid_by, user_id, -value_owed)

    return expense_id

  def print_user_balance_report(self, user_id):
    if(user_id not in self.user_dict):
      raise UserNotFoundException(user_id)

    user = self.user_dict[user_id]
    print(f"Overall situation of {user.name}:")
    if (user.total_balance == 0):
      print('\tYou are all set.')
    elif (user.total_balance > 0):
      print(f'\tYou are owed {user.total_balance}')
    else:
      print(f'\tYou owe {-user.total_balance}')

    print("Balance by user:")
    for balance in self.balance_users:
      if(user_id not in [balance.user_a, balance.user_b]):
        continue

      balance_value = balance.get_user_balance(user_id)
      other_user = self.user_dict[balance.get_counterparty_id(user_id)]
      if(balance_value > 0):
        print(f"\t{other_user.name} owes you a total of {balance_value}")
      elif(balance_value < 0):
        print(f"\tYou owe a total of {-balance_value} to {other_user.name}")

