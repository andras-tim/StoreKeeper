#!/bin/bash -e
cd "$(dirname "$0")/.."

function rebuild_docs()
{
    echo -e '\n[doc] Rebuilding...'
    set +e
    ./package.sh rebuild
    set -e

    date
}

rebuild_docs
while true
do
    inotifywait -r -qq -e modify,create,delete,move_self,delete_self \
        --exclude 'tmp' --exclude '_build' . ../VERSION.json ../server/app
    sleep 1
    rebuild_docs
done
