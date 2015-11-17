#!../flask/bin/python
import sys
import os.path
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(basedir)

from app.server import app, db


def main():
    migrations_path = os.path.abspath(os.path.join(basedir, 'db_migrations'))
    migrate = Migrate(app, db, directory=migrations_path)
    manager = Manager(app, with_default_commands=False)
    manager.add_command('db', MigrateCommand)

    manager.run()


if __name__ == '__main__':
    main()
