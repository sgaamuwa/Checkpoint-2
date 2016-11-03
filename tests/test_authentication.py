from authentication.authentication import Authentication
from database.models import User
from tests.test_setup import TestBaseCase

class AuthenticationTest(TestBaseCase):

    def test_register_user(self):
        # register a new user and see they are added to the database
        self.assertEqual(User.query.count(), 0)
        Authentication.register_user({"username": "user", "password": "password123"})
        self.assertEqual(User.query.count(), 1)

    def test_login_user(self):
        pass 

if __name__ == "__main__":
    unittest.main()