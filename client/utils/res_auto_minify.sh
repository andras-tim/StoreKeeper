#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -qq -e modify,create,delete app/css/src app/js/src
    utils/res_minify.sh
    date
done
