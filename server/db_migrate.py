#!flask/bin/python
from app.modules.database_maintenance import DatabaseMaintenance


if __name__ == "__main__":
    migration = DatabaseMaintenance.migrate()

    print('New migration saved as %s' % migration)
    print('Current database version: %d' % DatabaseMaintenance.get_version())
