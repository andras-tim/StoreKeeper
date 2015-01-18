#!/bin/bash -e
PYTHON_VERSION=3.4

function init()
{
    PIP='sudo pip3'
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PIP='flask/bin/pip'
    fi

    PYTHON="python${PYTHON_VERSION}"
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PYTHON='flask/bin/python'
    fi
}

function do_preinstall()
{
    packages="python${PYTHON_VERSION}"
    if [ "${GLOBAL_INSTALL}" == true ]
    then
        packages="${packages} python3-pip"
    else
        packages="${packages} python-virtualenv"
    fi
    sudo apt-get install ${packages}
}

function do_postinstall()
{
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        # Install virtualenv
        if [ ! -e flask ]
        then
            virtualenv -p python${PYTHON_VERSION} flask
        fi
    fi

    # Update Python packages
    "${PIP}" install --upgrade pip setuptools
    "${PIP}" install -r requirements.txt --upgrade
}

function do_clear()
{
    # Remove virtualenv
    if [ -e flask ]
    then
        rm -r flask
    fi
}

function do_start()
{
    "${PYTHON}" run.py
}


cd "$(dirname "$0")"
source ../.main.sh
