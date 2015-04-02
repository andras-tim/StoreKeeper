#!/bin/bash -e

function do_preinstall()
{
    if [ ! -e '/etc/apt/sources.list.d/nodesource.list' ]
    then
        wget -q 'https://deb.nodesource.com/setup' -O - | sudo bash -
    fi
    sudo apt-get install nodejs
}

function do_postinstall()
{
    if [ "${PRODUCTION}" == true ]
    then
        npm install --production
    else
        npm install
        npm run update-webdriver
    fi
    node_modules/bower/bin/bower install
}

function do_clear()
{
    if [ -e app/bower_components ]
    then
        rm -rf app/bower_components
    fi
    if [ -e node_modules ]
    then
        rm -rf node_modules
    fi
}


cd "$(dirname "$0")"
source ../.main.sh
