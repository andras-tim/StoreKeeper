import unittest

from app.server import app, config, db


class CommonTestWithDatabaseSupport(unittest.TestCase):
    """
    Super class of database based tests

    Initialize a brand-new database at start, and purge at stop.
    """
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

    def tearDown(self):
        CommonTestWithDatabaseSupport.tearDownClass()
        db.session.remove()
        db.drop_all()
        app.config['SQLALCHEMY_DATABASE_URI'] = config.Flask.SQLALCHEMY_DATABASE_URI
