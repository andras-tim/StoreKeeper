#!flask/bin/python
import os.path
from migrate.versioning import api

from app.server import config, db


def main():
    db.create_all()
    if not os.path.exists(config.App.MIGRATE_REPO_PATH):
        api.create(config.App.MIGRATE_REPO_PATH, 'database repository')
        api.version_control(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH)
    else:
        api.version_control(config.Flask.SQLALCHEMY_DATABASE_URI, config.App.MIGRATE_REPO_PATH,
                            api.version(config.App.MIGRATE_REPO_PATH))


if __name__ == "__main__":
    main()
