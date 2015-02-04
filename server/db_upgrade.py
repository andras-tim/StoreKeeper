#!flask/bin/python
from app.modules.database_maintenance import DatabaseMaintenance


if __name__ == "__main__":
    DatabaseMaintenance.upgrade()

    print('Current database version: %d' % DatabaseMaintenance.get_version())
