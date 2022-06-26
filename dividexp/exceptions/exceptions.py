class UserNotFoundException(Exception):
  def __init__(self, user_id):
    super().__init__(f'User with id {user_id} was not found.')
