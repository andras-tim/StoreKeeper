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
        wget -q 'https://deb.nodesource.com/setup_4.x' -O - | sudo bash -
    fi
    apt_get_install nodejs

    sudo npm install -g npm
}

function do_install()
{
    install_node_dependencies
    install_bower_dependencies

    if [ "${PRODUCTION}" == false ]
    then
        run update_webdriver
    fi

    mkdir -p tmp
    run resources
}

function install_node_dependencies()
{
    local args='--no-optional'

    if [ "${PRODUCTION}" == true ]
    then
        args="${args} --production"
    fi

    echo -e "\n$ npm install ${args}"
    npm install ${args}
}

function install_bower_dependencies()
{
    local args=

    if [ "${PRODUCTION}" == true ]
    then
        args="${args} --production"
    fi

    if [ "${FORCE}" == true ]
    then
        args="${args} --config.interactive=false"
    fi

    echo -e "\n$ bower install ${args}"
    node_modules/bower/bin/bower install ${args}
}

function do_resources()
{
    if [ "${PRODUCTION}" == true ]
    then
        node_modules/grunt-cli/bin/grunt "$@" --production
    else
        node_modules/grunt-cli/bin/grunt "$@"
    fi
}

function do_clear()
{
    purge app/dist
    purge node_modules
    purge bower_components
    purge tmp
}

function do_test()
{
    run check_style
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

function do_check_style()
{
    npm run jshint
    npm run jscs
}

cd "$(dirname "$0")"
source ../.main.sh
