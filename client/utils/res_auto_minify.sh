#!/bin/bash -e
while true
do
    inotifywait -qq -e modify,create,delete app/css app/js
    "$(dirname "$0")/res_minify.sh"
done
