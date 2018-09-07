import unittest
import json

from app import create_app
from app.model import User, db

SIGNUP_URL = '/api/v1/auth/signup'
LOGIN_URL = '/api/v1/auth/login'


class EntryClass(unittest.TestCase):
    """ This is EntryClass for test cases """

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_data = {
            "username": "danny",
            "email": "danny@gmail.com",
            "password": "test12345"
        }

        self.user1 = User(
            username='testuser',
            email='testuser@email.com',
            password='password')

        self.test_user = User(
            username='dannyb',
            email='dan@mail.com',
            password='pass12345')

    def logged_in_user(self):
        """ Create User """
        self.client.post(SIGNUP_URL,
                         data=json.dumps(self.user_data), content_type='application/json')

        """ User should be able to login """
        res = self.client.post(LOGIN_URL,
                               data=json.dumps(
                                   {'username': 'danny', 'password': 'test12345'}),
                               content_type='application/json')

        return res

    def tearDown(self):
        """ Drop the DATABASE structure """
        db.drop()


if __name__ == '__main__':
    unittest.main()