from typing import List
from src.exceptions.exceptions import UserNotFoundException
from enum import Enum

class ExpenseTypes(Enum):
  EQUAL = 1
  PERCENTAGE = 2
  VALUE = 3

class ExpenseBase:
  total_value: float
  used_by: List[int] = []
  description: str
  paid_by: int

  def __init__(self, paid_by=None, used_by=[], total_value=None, description=None):
    if(total_value <= 0):
      raise Exception('Expense value cannot be negative or zero.')

    if(len(used_by)== 0):
      raise Exception('Used by cannot be empty.')

    if(type(description) is not str or len(description) == 0):
      raise Exception('Description must be a valid string.')

    self.total_value = total_value
    self.description = description
    self.paid_by = paid_by
    self.used_by = used_by

  def _assert_valid_user(self, user_id):
    if (user_id != self.paid_by and user_id not in self.used_by):
      raise UserNotFoundException(user_id)

  def get_user_balance(self, user_id):
    raise Exception('Not implemented')

class ExpenseEqual(ExpenseBase):
  def __init__(self, total_value=None, description=None, paid_by=None, used_by=[]):
    super().__init__(paid_by, used_by, total_value, description)

  def get_user_balance(self, user_id):
    self._assert_valid_user(user_id)

    if (user_id in self.used_by):
      if (user_id == self.paid_by):
        return self.total_value * ((len(self.used_by) - 1) / len(self.used_by))

      return - ((1 / len(self.used_by)) * self.total_value)

    return self.total_value

class ExpensePercentage(ExpenseBase):
  percentage_used: List[float] = []

  def __init__(self, total_value=None, description=None, paid_by=[], used_by=[],percentage_used=[]):
    super().__init__(paid_by, used_by, total_value, description)
    if(len(used_by) != len(percentage_used)):
      raise Exception('Used list and percentage list must have the same length.')

    if (sum(percentage_used) != 100):
      raise Exception('Percentage total should be equal a 100.')

    self.percentage_used = percentage_used

  def get_user_balance(self, user_id):
    self._assert_valid_user(user_id)

    if (user_id in self.used_by):
      user_index = self.used_by.index(user_id)
      user_percentage = self.percentage_used[user_index]

      if (user_id == self.paid_by):
        return self.total_value - (user_percentage / 100 * self.total_value)

      return - (user_percentage / 100 * self.total_value)

    return self.total_value

class ExpenseValue(ExpenseBase):
  value_used: List[float] = []

  def __init__(self, total_value=None, description=None, paid_by=[], used_by=[], value_used=[]):
    super().__init__(paid_by, used_by, total_value, description)

    if(len(used_by) != len(value_used)):
      raise Exception('Used list and value list must have the same length.')

    if (sum(value_used) != self.total_value):
      raise Exception('Sum of used value must be equal total value.')

    self.value_used = value_used

  def get_user_balance(self, user_id):
    self._assert_valid_user(user_id)

    if (user_id in self.used_by):
      user_index = self.used_by.index(user_id)
      user_used_value = self.value_used[user_index]

      if (user_id == self.paid_by):
          return self.total_value - user_used_value

      return -user_used_value

    return self.total_value

class Expense:
  _expense: ExpenseBase
  id: int

  def __init__(self, id, expense_type: ExpenseTypes = None, **kwargs):
    self.id = id
    if(expense_type == ExpenseTypes.EQUAL):
      self._expense = ExpenseEqual(**kwargs)
    elif(expense_type == ExpenseTypes.PERCENTAGE):
      self._expense = ExpensePercentage(**kwargs)
    elif(expense_type == ExpenseTypes.VALUE):
      self._expense = ExpenseValue(**kwargs)
    else:
      raise Exception("Invalid Expense type.")

  def get_user_balance(self, user_id):
    return self._expense.get_user_balance(user_id)

  def get_paid_by(self):
    return self._expense.paid_by

  def get_used_by(self):
    return self._expense.used_by

  def get_expense(self):
    return self._expense