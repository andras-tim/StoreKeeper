import os
import re
import shutil
from _pytest.python import SubRequest
from _pytest.tmpdir import TempdirFactory
import pytest

from app.server import app, config
from app.modules.database_maintenance import DatabaseMaintenance


@pytest.fixture(scope='function')
def temp_db(request: SubRequest, tmpdir_factory: TempdirFactory):
    db_dir = tmpdir_factory.mktemp('db')
    database_uri = 'sqlite:///{}'.format(db_dir.join('test.sqlite'))
    migrate_repo_path = '{}'.format(db_dir.join('test_migrate_db'))

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db_maintenance = DatabaseMaintenance(database_uri=database_uri, migrate_repo_path=migrate_repo_path)
    cleanup_db_and_migrate_repo(db_maintenance)

    db_maintenance.create()

    def teardown():
        cleanup_db_and_migrate_repo(db_maintenance)
        app.config['SQLALCHEMY_DATABASE_URI'] = config.Flask.SQLALCHEMY_DATABASE_URI

    request.addfinalizer(teardown)
    return db_maintenance


def cleanup_db_and_migrate_repo(db_maintenance: DatabaseMaintenance):
    db_path = re.sub(r'^[^:]+:///(.+)$', r'\1', db_maintenance.database_uri)
    if db_path != ':memory:' and os.path.exists(db_path):
        os.remove(db_path)

    dir_path_of_db = os.path.dirname(db_path)
    if not os.path.exists(dir_path_of_db):
        os.mkdir(dir_path_of_db)

    if os.path.exists(config.App.MIGRATE_REPO_PATH):
        shutil.rmtree(config.App.MIGRATE_REPO_PATH)


def test_create(temp_db: DatabaseMaintenance):
    # The DatabaseMaintenance.create() call was ran in create_db() function fixture
    assert os.path.exists(temp_db.migrate_repo_path)
    assert temp_db.get_version() == 0


def test_migrate(temp_db: DatabaseMaintenance):
    temp_db.migrate()
    assert temp_db.get_version() == 1

    temp_db.migrate()
    assert temp_db.get_version() == 2


@pytest.fixture(scope='function')
def temp_db_version_2(temp_db: DatabaseMaintenance):
    temp_db.migrate()  # ver=1
    temp_db.migrate()  # ver=2
    return temp_db


def test_downgrade_version(temp_db_version_2: DatabaseMaintenance):
    temp_db_version_2.downgrade()
    assert temp_db_version_2.get_version() == 1

    temp_db_version_2.downgrade()
    assert temp_db_version_2.get_version() == 0


def test_upgrade_version(temp_db_version_2: DatabaseMaintenance):
    temp_db_version_2.downgrade()  # ver=1

    temp_db_version_2.upgrade()
    assert temp_db_version_2.get_version() == 2
