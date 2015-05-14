#!/bin/bash -e

function do_preinstall()
{
    apt_get_install wget
    if [ "${PRODUCTION}" == false ]
    then
        apt_get_install inotify-tools
    fi

    if [ ! -e '/etc/apt/sources.list.d/nodesource.list' ]
    then
        wget -q 'https://deb.nodesource.com/setup' -O - | sudo bash -
    fi
    apt_get_install nodejs
}

function do_install()
{
    if [ "${PRODUCTION}" == true ]
    then
        npm install --production
    else
        npm install
    fi
    node_modules/bower/bin/bower install

    if [ "${PRODUCTION}" == false ]
    then
        run update_webdriver
    fi

    mkdir -p tmp
    run minify
    run make_defaults
}

function do_minify()
{
    utils/res_minify.sh
}

function do_make_defaults()
{
    make_default 'app/ico/apple-touch-icon-114-precomposed' .png
    make_default 'app/ico/apple-touch-icon-144-precomposed' .png
    make_default 'app/ico/apple-touch-icon-72-precomposed' .png
    make_default 'app/ico/apple-touch-icon-57-precomposed' .png
    make_default 'app/ico/favicon' .png
    make_default 'app/img/label_logo' .gif
    make_default 'app/img/logo' .png
    make_default 'app/img/logo' .svg
}

function do_clear()
{
    purge node_modules
    purge app/bower_components
}

function do_test()
{
    run test_single_run
    run protractor
}

function do_test_continously()
{
    npm test "$@"
}

function do_test_single_run()
{
    npm run test-single-run "$@"
}

function do_update_webdriver()
{
    npm run update-webdriver "$@"
}

function do_protractor()
{
    echo 'Info: Have to run StoreKeeper server with default config'
    npm run protractor "$@"
}


cd "$(dirname "$0")"
source ../.main.sh
