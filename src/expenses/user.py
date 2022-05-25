class User:
  name: str
  id: int
  total_balance: float = 0

  def __init__(self, id, name):
    self.id = id
    self.name = name

  def add_balance(self, value: float):
    self.total_balance += value
