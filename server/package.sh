#!/bin/bash -e
PYTHON_VERSION=3.4

function init()
{
    PYTHON="python${PYTHON_VERSION}"
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PYTHON="$(pwd)/flask/bin/python"
    fi

    PIP='pip3'
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PIP="${PYTHON} -m pip"
    fi
}

function do_preinstall()
{
    # Extra dependencies for fast Yaml file reading (http://stackoverflow.com/a/24791419/1108919)
    packages="build-essential python${PYTHON_VERSION} python${PYTHON_VERSION}-dev libyaml-dev python3-cups python3-psycopg2"
    if [ "${GLOBAL_INSTALL}" == true ]
    then
        packages="${packages} python3-pip"
    else
        packages="${packages} python-virtualenv"
    fi
    apt_get_install ${packages}

    if [ "${GLOBAL_INSTALL}" == false ]
    then
        # Install virtualenv
        if [ ! -e flask ]
        then
            virtualenv --system-site-packages -p python${PYTHON_VERSION} flask
        fi
    fi
    ${PIP} install --upgrade pip setuptools
}

function do_install()
{
    ${PIP} install -r requirements.txt --upgrade
    if [ "${PRODUCTION}" == false ]
    then
        ${PIP} install -r requirements-dev.txt --upgrade
    fi

    mkdir -p tmp
}

function do_clear()
{
    purge tmp
    purge flask
    purge test/.cache
    find_and_purge . -name __pycache__
}

function do_start()
{
    ${PYTHON} run.py
}

function do_test()
{
    export PYTHON
    utils/test.sh "$@"
}

function do_manage_database()
{
    ${PYTHON} utils/database.py "$@"
}

function do_fill_up_database()
{
    ${PYTHON} utils/fill_up.py "$@"
}

cd "$(dirname "$0")"
source ../.main.sh
