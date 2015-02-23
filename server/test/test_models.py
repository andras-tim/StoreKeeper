import unittest

from app.server import bcrypt
from app.models import User


class TestUser(unittest.TestCase):
    _USER = "foo"
    _PASSWORD = "secret_pass"
    _EMAIL = "foo@bar"

    def setUp(self):
        self.user = User(TestUser._USER, TestUser._PASSWORD, TestUser._EMAIL)

    def test_password_is_not_stored_plain_text(self):
        self.assertNotEqual(TestUser._PASSWORD, self.user.password)
        self.assertIsNotNone(self.user.password)

    def test_password_is_able_to_check(self):
        self.assertTrue(bcrypt.check_password_hash(self.user.password, TestUser._PASSWORD))
