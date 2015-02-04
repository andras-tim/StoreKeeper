import os
import re
import shutil
import unittest

from app.server import config
from app.modules.database_maintenance import DatabaseMaintenance


class TestDatabaseCreate(unittest.TestCase):
    def tearDown(self):
        _cleanup_db_and_migrate_repo()

    def test_create(self):
        DatabaseMaintenance.create()

        self.assertTrue(os.path.exists(config.App.MIGRATE_REPO_PATH))
        self.assertEqual(0, DatabaseMaintenance.get_version())


class TestDatabaseMigrate(unittest.TestCase):
    def setUp(self):
        DatabaseMaintenance.create()

    def tearDown(self):
        _cleanup_db_and_migrate_repo()

    def test_migrate(self):
        DatabaseMaintenance.migrate()
        self.assertEqual(1, DatabaseMaintenance.get_version())

        DatabaseMaintenance.migrate()
        self.assertEqual(2, DatabaseMaintenance.get_version())


class TestDatabaseSwitchVersion(unittest.TestCase):
    def setUp(self):
        DatabaseMaintenance.create()  # ver=0
        DatabaseMaintenance.migrate()  # ver=1
        DatabaseMaintenance.migrate()  # ver=2

    def tearDown(self):
        _cleanup_db_and_migrate_repo()

    def test_downgrade(self):
        DatabaseMaintenance.downgrade()
        self.assertEqual(1, DatabaseMaintenance.get_version())

        DatabaseMaintenance.downgrade()
        self.assertEqual(0, DatabaseMaintenance.get_version())

    def test_upgrade(self):
        DatabaseMaintenance.downgrade()  # ver=1

        DatabaseMaintenance.upgrade()
        self.assertEqual(2, DatabaseMaintenance.get_version())


def _cleanup_db_and_migrate_repo():
    db_path = re.sub(r'^[^:]+:///(.+)$', r'\1', config.Flask.SQLALCHEMY_DATABASE_URI)
    if db_path != ":memory:" and os.path.exists(db_path):
        os.remove(db_path)

    if os.path.exists(config.App.MIGRATE_REPO_PATH):
        shutil.rmtree(config.App.MIGRATE_REPO_PATH)
