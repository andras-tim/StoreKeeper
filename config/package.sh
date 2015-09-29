#!/bin/bash -e

function do_make_defaults()
{
    echo " * Server"
    make_default 'config.default' .yml

    echo " * Client"
    make_default 'img/label_logo' .gif
    make_default 'img/logo' .png
    make_default 'img/logo' .svg
    make_default 'img/background' .svg
    make_default 'ico/apple-touch-icon-114-precomposed' .png
    make_default 'ico/apple-touch-icon-144-precomposed' .png
    make_default 'ico/apple-touch-icon-72-precomposed' .png
    make_default 'ico/apple-touch-icon-57-precomposed' .png
    make_default 'ico/favicon' .png
}


cd "$(dirname "$0")"
source ../.main.sh
