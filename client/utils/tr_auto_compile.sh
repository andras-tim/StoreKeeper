#!/bin/bash -e
cd "$(dirname "$0")/.."
while true
do
    inotifywait -r -qq -e modify po/hu.po
    sleep 1

    echo -e '\n[client] Compiling translation files...'
    set +e
    utils/tr_compile.sh
    set -e

    date
done
