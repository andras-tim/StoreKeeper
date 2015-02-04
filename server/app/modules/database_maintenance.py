import os.path
import imp
from migrate.versioning import api

from app.server import db, config


class DatabaseMaintenance(object):
    __database_uri = config.Flask.SQLALCHEMY_DATABASE_URI
    __migrate_repo_path = config.App.MIGRATE_REPO_PATH

    @classmethod
    def create(cls):
        db.create_all()
        if not os.path.exists(cls.__migrate_repo_path):
            api.create(cls.__migrate_repo_path, 'database repository')
            api.version_control(cls.__database_uri, cls.__migrate_repo_path)
        else:
            api.version_control(cls.__database_uri, cls.__migrate_repo_path, api.version(cls.__migrate_repo_path))

    @classmethod
    def downgrade(cls):
        db_version = cls.__get_version()
        api.downgrade(cls.__database_uri, cls.__migrate_repo_path, db_version - 1)
        db_version = cls.__get_version()

        cls.__show_results(db_version)

    @classmethod
    def migrate(cls):
        db_version = cls.__get_version()
        migration = '%s/versions/%03d_migration.py' % (cls.__migrate_repo_path, db_version + 1)

        tmp_module = imp.new_module('old_model')
        old_model = api.create_model(cls.__database_uri, cls.__migrate_repo_path)
        exec(old_model, tmp_module.__dict__)

        script = api.make_update_script_for_model(
            cls.__database_uri, cls.__migrate_repo_path,
            tmp_module.meta, db.metadata
        )
        with open(migration, "wt") as fd:
            fd.write(script)
        api.upgrade(cls.__database_uri, cls.__migrate_repo_path)
        db_version = cls.__get_version()

        cls.__show_results(db_version, 'New migration saved as %s' % migration)

    @classmethod
    def upgrade(cls):
        api.upgrade(cls.__database_uri, cls.__migrate_repo_path)
        db_version = cls.__get_version()

        cls.__show_results(db_version)

    @classmethod
    def __get_version(cls) -> int:
        return api.db_version(cls.__database_uri, cls.__migrate_repo_path)

    @classmethod
    def __show_results(cls, db_version: int, process_specific_info: str=None):
        if process_specific_info:
            print(process_specific_info)
        print('Current database version: %d' % db_version)

