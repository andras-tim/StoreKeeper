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
    packages="build-essential python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python3-pip libjpeg-dev libffi-dev zlib1g-dev libyaml-dev python3-cups python3-psycopg2 fonts-dejavu"
    if [ "${GLOBAL_INSTALL}" == false ]
    then
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
    ${PIP} install --upgrade pip setuptools wheel
}

function do_install()
{
    mkdir -p tmp

    pip_options='--upgrade'
    if [ -e "tmp/pip-download-cache" ]
    then
        mkdir -p "$(pwd)/tmp/pip-download-cache"
        pip_options="${pip_options} --cache-dir $(pwd)/tmp/pip-download-cache"
    fi

    ${PIP} install -r requirements.txt ${pip_options}
    if [ "${PRODUCTION}" == false ]
    then
        ${PIP} install -r requirements-dev.txt ${pip_options}
    fi
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
    ${PYTHON} utils/database.py db "$@"
}

function do_fill_up_database()
{
    ${PYTHON} utils/fill_up.py "$@"
}

cd "$(dirname "$0")"
source ../.main.sh
