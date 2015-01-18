#!flask/bin/python
from migrate.versioning import api

from app.server import config


def main():
    api.upgrade(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)
    db_version = api.db_version(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)

    print('Current database version: %d' % db_version)


if __name__ == "__main__":
    main()
