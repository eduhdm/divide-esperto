from typing import List
from src.expenses.user import User
from enum import Enum

class ExpenseTypes(Enum):
  EQUAL = 1
  PERCENTAGE = 2
  VALUE = 3

class Expense:
  id: int
  paid_by: int
  used_by: List[int] = []
  total_value: float
  description: str

  def __init__(self, id, paid_by=None, used_by=[], total_value=None, description=None):
    self.id = id
    self.paid_by = paid_by
    self.used_by = used_by
    self.total_value = total_value
    self.description = description

  def get_user_balance(self, user_id):
    if (user_id == self.paid_by):
      if (user_id in self.used_by):
        return self.total_value * ((len(self.used_by) - 1) / len(self.used_by))

      return self.total_value


    return - ((1 / len(self.used_by)) * self.total_value)
