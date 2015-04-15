#!/bin/bash -e
BASEDIR="$(dirname "$0")"

function run_test()
{
    "${BASEDIR}/flask/bin/py.test" --durations=3 --ff "$@" "${BASEDIR}/test"
}

function run_test_with_coverage()
{
    run_test --cov "${BASEDIR}/app" --cov-config "${BASEDIR}/.coveragerc" --cov-report=term-missing "$@"
}

function run_pep8_check()
{
    "${BASEDIR}/flask/bin/python3" -m pep8 --max-line-length=120 --ignore=E402 "${BASEDIR}/app" "${BASEDIR}/test"
}

function run_pylint()
{
    "${BASEDIR}/flask/bin/python3" -m pylint --rcfile "${BASEDIR}/.pylintrc" "${BASEDIR}/app" "${BASEDIR}/test"
}

function show_help()
{
    cat - << EOF
Run tests and coverage

$(basename "$0") [arg]

Available arguments:
  -h, --help            Show this help
  -f, --fast            Parallel run tests (single threaded tests will be skipped)
  -q, --quick           Parallel run quick-test (single threaded and rights tests will be skipped)

EOF
}

function get_count_of_cpu_cores()
{
    getconf _NPROCESSORS_ONLN
}

function get_parallel_run_options()
{
    echo "-n $[$(get_count_of_cpu_cores) - 1]"
}


# Main
FAST=false
QUICK=false
if [ $# -gt 0 ]
then
    case "$1" in
        -h|--help)  show_help
                    exit 0
                    ;;
        -f|--fast)  FAST=true
                    shift
                    ;;
        -q|--quick) QUICK=true
                    shift
                    ;;
    esac
fi

if [ "${FAST}" == 'true' ]
then
    run_test_with_coverage -m 'not single_threaded' $(get_parallel_run_options) "$@"
elif [ "${QUICK}" == 'true' ]
then
    run_test_with_coverage -m 'not single_threaded and not rights_test' $(get_parallel_run_options) "$@"
else
    run_test_with_coverage --exitfirst --pdb "$@"
fi

echo -e "\nChecking PEP8 compliance..."
run_pep8_check
echo "passed"

if [ "${QUICK}" != 'true' ]
then
    echo -e "\nRunning pylint..."
    run_pylint
    echo "passed"
fi

echo -e "\nAll done"
exit 0
