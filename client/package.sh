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

    if [ "${FORCE}" == true ]
    then
        node_modules/bower/bin/bower install --config.interactive=false
    else
        node_modules/bower/bin/bower install
    fi

    if [ "${PRODUCTION}" == false ]
    then
        run update_webdriver
    fi

    mkdir -p tmp
    run minify
}

function do_minify()
{
    utils/res_minify.sh
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
    run check_style
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

function do_check_style()
{
    npm run jshint
    npm run jscs
}

cd "$(dirname "$0")"
source ../.main.sh
