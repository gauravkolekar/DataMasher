from application import mongodb


class User(object):
    """
    This class represent the user collection. It has two functions add_user and update_user
    add_user
    Inputs:
    firstname, lastname, email, password

    update_user
    Inputs:

    """

    def __init__(self):
        self.user = mongodb.db.user

    def add_user(self, firstname=None, lastname=None, email=None, password=None):
        self.user.insert({'firstname': firstname,
                          'lastname': lastname,
                          'email': email,
                          'password': password})

    def update_user(self):
        pass
