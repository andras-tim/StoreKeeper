import os.path
import imp
from migrate.versioning import api

from app.server import app, db, config


class DatabaseMaintenance:
    def __init__(self, database_uri: (str, None)=None, migrate_repo_path: (str, None)=None):
        self.__database_uri = database_uri or config.Flask.SQLALCHEMY_DATABASE_URI
        self.__migrate_repo_path = migrate_repo_path or config.App.MIGRATE_REPO_PATH

    @property
    def database_uri(self) -> str:
        return self.__database_uri

    @property
    def migrate_repo_path(self) -> str:
        return self.__migrate_repo_path

    def create(self):
        db.create_all()
        if not os.path.exists(self.__migrate_repo_path):
            api.create(self.__migrate_repo_path, 'database repository')
            api.version_control(self.__database_uri, self.__migrate_repo_path)
        else:
            api.version_control(self.__database_uri, self.__migrate_repo_path, api.version(self.__migrate_repo_path))

    def migrate(self):
        db_version = self.get_version()
        migration = '{!s}/versions/{:0>3d}_migration.py'.format(self.__migrate_repo_path, db_version + 1)

        tmp_module = imp.new_module('old_model')
        old_model = api.create_model(self.__database_uri, self.__migrate_repo_path)
        exec(old_model, tmp_module.__dict__)

        script = api.make_update_script_for_model(
            self.__database_uri, self.__migrate_repo_path,
            tmp_module.meta, db.metadata
        )
        with open(migration, 'wt') as fd:
            fd.write(script)
        api.upgrade(self.__database_uri, self.__migrate_repo_path)

        return migration

    def downgrade(self):
        db_version = self.get_version()
        api.downgrade(self.__database_uri, self.__migrate_repo_path, db_version - 1)

    def upgrade(self):
        api.upgrade(self.__database_uri, self.__migrate_repo_path)

    def get_version(self) -> int:
        return api.db_version(self.__database_uri, self.__migrate_repo_path)
