#!flask/bin/python
import imp
from migrate.versioning import api

from app.server import config, db


def main():
    db_version = api.db_version(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)
    migration = '%s/versions/%03d_migration.py' % (config.App.MIGRATE_REPO_PATH, db_version + 1)

    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)
    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH,
                                              tmp_module.meta, db.metadata)
    with open(migration, "wt") as fd:
        fd.write(script)
    api.upgrade(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)
    db_version = api.db_version(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)

    print('New migration saved as %s' % migration)
    print('Current database version: %d' % db_version)


if __name__ == "__main__":
    main()
