from src.expenses.group import Group

def main():
  group = Group()
  edu_id = group.add_user('Edu')
  salim_id = group.add_user('Salim')
  lukinhas_id = group.add_user('Lukinhas')

  group.add_expense(
    paid_by=edu_id,
    used_by=[edu_id, salim_id, lukinhas_id],
    total_value=300,
    description='Cerveja'
  )

  group.add_expense(
    paid_by=salim_id,
    used_by=[edu_id, salim_id, lukinhas_id],
    total_value=90,
    description='Cachaça'
  )

  group.print_user_balance_report(edu_id)
  print('----------------')
  group.print_user_balance_report(salim_id)
  print('----------------')
  group.print_user_balance_report(lukinhas_id)
  print('----------------')

main()
