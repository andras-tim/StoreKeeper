#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -r -qq -e modify,create,delete app/css/src app/js/src
    sleep 1

    echo -e '\n[client] Minifing resource files...'
    set +e
    utils/res_minify.sh
    set -e

    date
done
