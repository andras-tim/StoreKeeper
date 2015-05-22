#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -qq -e modify,create,delete app/css/src app/js/src

    set +e
    utils/res_minify.sh
    set -e

    date
done
