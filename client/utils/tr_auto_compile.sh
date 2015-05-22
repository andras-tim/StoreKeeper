#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -qq -e modify po/hu.po
    utils/tr_compile.sh
    date
done
