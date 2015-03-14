#!/bin/bash -e
BASEDIR="$(dirname "$0")"

function run_test()
{
    "${BASEDIR}/flask/bin/py.test" --durations=3 "$@" "${BASEDIR}/test"
}

function run_coverage()
{
    run_test --cov "${BASEDIR}/app" --cov-config "${BASEDIR}/.coveragerc" --cov-report=term-missing "$@"
}

function show_help()
{
    cat - << EOF
Run tests and coverage

$(basename "$0") [arg]

Available arguments:
  -h, --help            Show this help
  -f, --fast            Run tests parallel (single threaded tests will be skipped)

EOF
}

function get_count_of_cpu_cores()
{
    getconf _NPROCESSORS_ONLN
}


# Main
FAST=false
if [ $# -gt 0 ]
then
    case "$1" in
        -h|--help)  show_help
                    exit 0
                    ;;
        -f|--fast)  FAST=true
                    shift
                    ;;
    esac
fi

if [ "${FAST}" == 'true' ]
then
    run_coverage -m 'not single_threaded' -n $[$(get_count_of_cpu_cores) + 1] "$@"
else
    run_coverage -v --pdb "$@"
fi
exit 0
