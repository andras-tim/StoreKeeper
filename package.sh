#!/bin/bash -e

function do_install()
{
    server/package.sh preinstall
    client/package.sh preinstall

    server/package.sh install
    client/package.sh install

    config/package.sh make_defaults

    echo -e "\nAll Done!"
}

function do_create_database()
{
    server/package.sh manage_database --create
}

function do_make_defaults()
{
    config/package.sh make_defaults
}

function do_start()
{
    server/package.sh start
}

function do_clear()
{
    server/package.sh clear
    client/package.sh clear
    docs/package.sh clear
}

function do_docs()
{
    docs/package.sh rebuild
    docs/package.sh start
}


cd "$(dirname "$0")"
source .main.sh
