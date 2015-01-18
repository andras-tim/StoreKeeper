#!/bin/bash -e

function do_install()
{
    server/package.sh preinstall

    server/package.sh postinstall
}

function do_start()
{
    server/package.sh start
}

function do_clear()
{
    server/package.sh clear
}


cd "$(dirname "$0")"
source .main.sh
