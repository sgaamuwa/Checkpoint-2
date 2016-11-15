from app.authentication import Authentication
from app.models import User
from tests.test_setup import TestBaseCase


class AuthenticationTest(TestBaseCase):

    def test_register_user(self):
        """tests that a user is created and added to the database"""
        # assert that the database is empty
        self.assertEqual(User.query.count(), 2)
        # register a new user
        Authentication.register_user({
            "username": "user",
            "password": "password123"
            })
        # assert that the database is incremented by one
        self.assertEqual(User.query.count(), 3)

    def test_login_user(self):
        """tests that a registered user logs into the system"""
        # create a new user
        Authentication.register_user({
            "username": "user",
            "password": "password123"
            })
        # log user into the system
        login = Authentication.login_user({
            "username": "user",
            "password": "password123"
            })
        # assert that they logged in
        self.assertTrue(login)
        # log in with wrong password
        login = Authentication.login_user({
            "username": "user",
            "password": "password"
            })
        # assert that the login is false
        self.assertFalse(login)
