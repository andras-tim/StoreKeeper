#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -qq -e modify,create,delete app/css app/js
    utils/res_minify.sh
    date
done
