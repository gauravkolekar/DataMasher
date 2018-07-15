import secrets
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
        self.api_key = None

    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def _generate_key():
        return secrets.token_urlsafe(64)

    def verify_key(self, client_key):
        return self.user.find({'api_key': client_key}).count()

    def get_user_id(self, client_key):
        return list(self.user.find({'api_key': client_key}, {'_id': 1}))[0]['_id']

    def validate_email(self, email):
        return self.user.find({'email': email})

    def add_user(self, firstname=None, lastname=None, email=None, password=None):
        self.api_key = self._generate_key()
        self.user.insert({'firstname': firstname, 'lastname': lastname, 'email': email,
                          'password': self._hash_password(password), 'api_key': self.api_key})
        return self.api_key

    def update_user(self, email, password):
        self.user.update({'email': email}, {'$set': {'password': password,
                                                     'api_key': self._generate_key()}}, upsert=False)
