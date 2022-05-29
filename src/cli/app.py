from cmd import Cmd

from src.expenses.group import Group
from src.expenses.expense import ExpenseTypes

class ShellController():
    def __init__(self):
        self.group = Group()

    def add_user(self, user_name):
        return self.group.add_user(user_name)

    def create_exp(self, exp_type, total_value, description, paid_by, used_by,
            percentage_used=[], value_used=[]):

        if exp_type == "equal":
            exp_type = ExpenseTypes.EQUAL

            exp = self.group.add_expense(
                expense_type=exp_type,
                total_value=total_value,
                description=description,
                paid_by=paid_by,
                used_by=used_by,
            )

        if exp_type == "percentage":
            exp_type = ExpenseTypes.PERCENTAGE

            exp = self.group.add_expense(
                expense_type=exp_type,
                total_value=total_value,
                description=description,
                paid_by=paid_by,
                used_by=used_by,
                percentage_used=percentage_used,
            )

        if exp_type == "value":
            exp_type = ExpenseTypes.VALUE

            exp = self.group.add_expense(
                expense_type=exp_type,
                total_value=total_value,
                description=description,
                paid_by=paid_by,
                used_by=used_by,
                value_used=value_used,
            )

        return exp

    def print_user_balance_report(self, user_id):
        report = self.group.get_user_balance_report(user_id)
        print(report)

class InteractiveShell(Cmd):

    controller = ShellController()
    prompt = 'divide> '
    intro = "Welcome! Type ? to list available commands"

    def do_exit(self, inp):
        print("Exiting")
        return True

    def do_adduser(self, inp):
        print("Adding '{}'".format(inp))
        self.controller.add_user(inp)
        print("User '{}' added".format(inp))

    def help_adduser(self):
        print("Adds a user to the Group")
        print("Format: \n>adduser <user-name>")
        print("Example: \n>adduser Eduardo")

    def do_addexpense(self, inp):

        exp_type = input("addexpense> type (one of equal, percentage, value): ")
        total_value = int(input("addexpense> total value: "))
        description = input("addexpense> description: ")
        paid_by = int(input("addexpense> paid by: "))
        used_by = input("addexpense> used by: ")

        used_by = [int(user) for user in used_by.split(' ')]

        percentage_used = []
        value_used = []

        if exp_type == "percentage":
            percentage_used = input("addexpense> percentage used: ")
            percentage_used = [int(per) for per in percentage_used.split(' ')]
        if exp_type == "value":
            value_used = input("addexpense> valued used: ")
            value_used = [int(val) for val in value_used.split(' ')]

        self.controller.create_exp(
            exp_type,
            total_value,
            description,
            paid_by,
            used_by,
            percentage_used,
            value_used,
        )

    def help_addexpense(self):
        print("Adds an expense to the Group")
        # @TODO: write a description of the input

    def do_get_user_balance(self, inp):
        self.controller.print_user_balance_report(int(inp))

    def help_get_user_balance(self):
        print("Prints the balance of the user")
        # @TODO: write a description of the input

    do_EOF = do_exit

def main():
    InteractiveShell().cmdloop()
