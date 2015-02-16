import os
import re
import shutil
import unittest

from app.server import config
from app.modules.database_maintenance import DatabaseMaintenance


class CommonDatabaseMaintenanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._cleanup_db_and_migrate_repo()

    def setUp(self):
        DatabaseMaintenance.create()

    def tearDown(self):
        CommonDatabaseMaintenanceTest._cleanup_db_and_migrate_repo()

    @classmethod
    def _cleanup_db_and_migrate_repo(cls):
        db_path = re.sub(r'^[^:]+:///(.+)$', r'\1', config.Flask.SQLALCHEMY_DATABASE_URI)
        if db_path != ":memory:" and os.path.exists(db_path):
            os.remove(db_path)

        if os.path.exists(config.App.MIGRATE_REPO_PATH):
            shutil.rmtree(config.App.MIGRATE_REPO_PATH)


class TestCreateWithDatabaseSupport(CommonDatabaseMaintenanceTest):
    def test_create(self):
        # The DatabaseMaintenance.create() call was ran in super().setUp()
        self.assertTrue(os.path.exists(config.App.MIGRATE_REPO_PATH))
        self.assertEqual(0, DatabaseMaintenance.get_version())


class TestMigrateWithDatabaseSupport(CommonDatabaseMaintenanceTest):
    def test_migrate(self):
        DatabaseMaintenance.migrate()
        self.assertEqual(1, DatabaseMaintenance.get_version())

        DatabaseMaintenance.migrate()
        self.assertEqual(2, DatabaseMaintenance.get_version())


class TestSwitchVersionWithDatabaseSupport(CommonDatabaseMaintenanceTest):
    def setUp(self):
        super().setUp()
        DatabaseMaintenance.migrate()  # ver=1
        DatabaseMaintenance.migrate()  # ver=2

    def test_downgrade(self):
        DatabaseMaintenance.downgrade()
        self.assertEqual(1, DatabaseMaintenance.get_version())

        DatabaseMaintenance.downgrade()
        self.assertEqual(0, DatabaseMaintenance.get_version())

    def test_upgrade(self):
        DatabaseMaintenance.downgrade()  # ver=1

        DatabaseMaintenance.upgrade()
        self.assertEqual(2, DatabaseMaintenance.get_version())
