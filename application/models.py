from application import mongodb
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    """
    This class represent the user collection. It has two functions add_user and update_user
    """
    def __init__(self):
        self.user = mongodb.db.user
        self.firstname = None
        self.lastname = None
        self.email = None
        self.password = None
        self.password_hash = None

    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password)

    def check_password(self, email, password):
        return check_password_hash(self.user.findOne({'email': email}, {'_id': 0, 'password': 1}), password)

    def validate_email(self, email):
        return self.user.find({'email': email})

    def add_user(self, firstname=None, lastname=None, email=None, password=None):
        self.user.insert({'firstname': firstname, 'lastname': lastname, 'email': email,
                          'password': self._hash_password(password)})

    def update_user(self, email, password):
        self.user.update({'email': email}, {'$set': {'password': password}}, upsert=False)
