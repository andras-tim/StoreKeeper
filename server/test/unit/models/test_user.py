import unittest

from app.models import User


class TestUser(unittest.TestCase):
    _USER = 'foo'
    _PASSWORD = 'secret_pass'
    _EMAIL = 'foo@bar.com'

    def setUp(self):
        self.user = User(username=TestUser._USER, email=TestUser._EMAIL)
        self.user.set_password(TestUser._PASSWORD)

    def test_password_is_not_stored_plain_text(self):
        self.assertNotEqual(TestUser._PASSWORD, self.user.password_hash)
        self.assertIsNotNone(self.user.password_hash)

    def test_password_is_able_to_check(self):
        self.assertTrue(self.user.check_password(TestUser._PASSWORD))
