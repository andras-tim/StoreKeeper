#!/bin/bash -e
BASEDIR="$(dirname "$0")"

function run_test()
{
    "${BASEDIR}/flask/bin/py.test" --durations=3 "$@" "${BASEDIR}/test"
}

function run_coverage()
{
    run_test --cov "${BASEDIR}/app" --cov-config "${BASEDIR}/.coveragerc" --cov-report=term-missing --cov-report=html "$@"
}

run_coverage --pdb
exit 0
