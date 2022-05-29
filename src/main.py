from src.expenses.expense import ExpenseTypes
from src.expenses.group import Group

def main():
  group = Group()
  edu_id = group.add_user('Edu')
  salim_id = group.add_user('Salim')
  lukinhas_id = group.add_user('Lukinhas')

  group.add_expense(
    expense_type=ExpenseTypes.PERCENTAGE,
    paid_by=edu_id,
    used_by=[edu_id, salim_id, lukinhas_id],
    percentage_used=[50, 20, 30],
    total_value=300,
    description='Cerveja'
  )

  group.add_expense(
    expense_type=ExpenseTypes.PERCENTAGE,
    paid_by=salim_id,
    used_by=[edu_id, salim_id, lukinhas_id],
    percentage_used=[50, 20, 30],
    total_value=90,
    description='Cachaça'
  )

  print(group.get_user_balance_report(edu_id))
  print('----------------')
  print(group.get_user_balance_report(salim_id))
  print('----------------')
  print(group.get_user_balance_report(lukinhas_id))
  print('----------------')

if __name__ == '__main__':
  main()
