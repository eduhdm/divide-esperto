from exceptions.exceptions import UserNotFoundException

class Balance:
  user_a: int
  user_b: int
  amount_paid_a: float
  amount_paid_b: float

  def __init__(self, user_a, user_b, amount_paid_a, amount_paid_b):
    self.user_a = user_a
    self.user_b = user_b
    self.amount_paid_a = amount_paid_a
    self.amount_paid_b = amount_paid_b

  def add_amount(self, user_id, amount):
    if(user_id == self.user_a):
      self.amount_paid_a += amount
      return
    if(user_id == self.user_b):
      self.amount_paid_b += amount
      return

    raise UserNotFoundException(user_id)


  def get_user_balance(self, user_id):
    if(user_id == self.user_a):
      return self.amount_paid_a - self.amount_paid_b
    if(user_id == self.user_b):
      return self.amount_paid_b - self.amount_paid_a

    raise UserNotFoundException(user_id)

  def get_counterparty_id(self, user_id):
    if(user_id == self.user_a):
      return self.user_b
    if(user_id == self.user_b):
      return self.user_a

    raise UserNotFoundException(user_id)
