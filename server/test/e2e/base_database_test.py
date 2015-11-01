import unittest

from app.server import app, db


class CommonTestWithDatabaseSupport(unittest.TestCase):
    """
    Super class of database based tests

    Initialize a brand-new database at start, and purge at stop.
    """
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        CommonTestWithDatabaseSupport.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
