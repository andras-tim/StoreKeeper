#!./flask/bin/python
import argparse
import sys

from app.server import db
from app.models import User
from app.modules.database_maintenance import DatabaseMaintenance


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Database maintenance")
    command = parser.add_mutually_exclusive_group()

    command.add_argument("--create", action="store_true", help="create empty database from model")
    command.add_argument("--migrate", action="store_true", help="migrate database to schema from model")
    command.add_argument("--downgrade", action="store_true", help="downgrade database to previous version")
    command.add_argument("--upgrade", action="store_true", help="upgrade database to next version")
    command.add_argument("-v", "--version", action="store_true", help="get version of current database")

    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.create:
        DatabaseMaintenance.create()
        db.session.add(User(username="admin", password="admin", email="admin@localhost", admin=True))
        db.session.commit()
        print("Done")

    elif args.migrate:
        migration = DatabaseMaintenance.migrate()
        print('New migration saved as %s' % migration)

    elif args.downgrade:
        DatabaseMaintenance.downgrade()

    elif args.upgrade:
        DatabaseMaintenance.upgrade()

    elif args.version:
        pass

    print('Current database version: %d' % DatabaseMaintenance.get_version())
    return 0


if __name__ == "__main__":
    sys.exit(main())
