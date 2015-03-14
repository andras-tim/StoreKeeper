#!/bin/bash -e

function do_install()
{
    make html
}

function do_start()
{
    xdg-open _build/html/index.html
}

function do_clear()
{
    purge '_build'
}

function do_reinstall()
{
    do_clear
    do_install
}


cd "$(dirname "$0")"
source ../.main.sh
