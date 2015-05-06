#!/bin/bash
while true
do
    inotifywait -qq -e modify po/hu.po
    "$(dirname "$0")/tr_compile.sh"
done
