#!/bin/bash -e
UNRELEASED_TAG='unreleased'
cd "$(dirname "$0")/.."

function upgrade_db()
{
    set +e

    echo -e '\n[db] Migrating...'
    find 'db_migrations/versions' -maxdepth 1 -name "*_${UNRELEASED_TAG}.py" -exec rm {} \;
    ./package.sh manage_database migrate -m "${UNRELEASED_TAG}"

    set -e
    date
}

upgrade_db
while true
do
    inotifywait -r -qq -e modify,create,delete,move_self,delete_self \
        --exclude 'db_migrations/versions' app db_migrations utils
    sleep 1
    upgrade_db
done
