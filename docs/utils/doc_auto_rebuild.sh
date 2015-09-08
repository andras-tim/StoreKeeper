#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -r -qq -e modify,create,delete . ../server/app
    sleep 1

    echo -e '\n[doc] Rebuilding...'
    set +e
    ./package.sh rebuild
    set -e

    date
done
