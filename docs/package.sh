#!/bin/bash -e

function do_clear()
{
    purge _build
}

function do_build()
{
    make html
}

function do_rebuild()
{
    run clear
    run build
}

function do_start()
{
    xdg-open _build/html/index.html
}

function do_render_db_model()
{
    ../server/flask/bin/python3 'utils/db_model_renderer.py' "$@"
}


cd "$(dirname "$0")"
source ../.main.sh
