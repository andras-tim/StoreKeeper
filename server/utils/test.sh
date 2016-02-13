#!/bin/bash -e
BASEDIR="$(cd "$(dirname "$0")/.."; pwd)"
PYTHON=${PYTHON:-${BASEDIR}/flask/bin/python3}

function run_test()
{
    "${PYTHON}" -m pytest -c "${BASEDIR}/test/pytest.ini" --basetemp "${BASEDIR}/tmp" --durations=10 --ff "$@" "${BASEDIR}/test"
}

function run_test_with_coverage()
{
    run_test --cov "${BASEDIR}/app" --cov-config "${BASEDIR}/.coveragerc" --cov-report=term-missing "$@"
}

function run_pep8_check()
{
    echo -e "\nChecking PEP8 compliance..."
    "${PYTHON}" -m pep8 --max-line-length=120 --ignore=E402 "${BASEDIR}/app" "${BASEDIR}/utils" "${BASEDIR}/test"
    echo "passed"
}

function run_pylint()
{
    echo -e "\nRunning pylint..."
    "${PYTHON}" -m pylint --rcfile "${BASEDIR}/.pylintrc" "${BASEDIR}/app" "${BASEDIR}/utils" "${BASEDIR}/test"
    echo "passed"
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
  -p, --pep8            Run PEP8 check only
  -l, --pylint          Run pylint only

EOF
}

function get_count_of_cpu_cores()
{
    getconf _NPROCESSORS_ONLN
}

function get_parallel_run_options()
{
    local thread_count="$(get_count_of_cpu_cores)"

    if [ "${thread_count}" -gt 8 ]
    then
        thread_count=8
    fi
    echo "-n ${thread_count}"
}


# Main
cd -P "${BASEDIR}"

FAST=false
QUICK=false
if [ $# -gt 0 ]
then
    case "$1" in
        -h|--help)      show_help
                        exit 0
                        ;;
        -f|--fast)      FAST=true
                        shift
                        ;;
        -q|--quick)     QUICK=true
                        shift
                        ;;
        -p|--pep8)      run_pep8_check
                        exit 0
                        ;;
        -l|--pylint)    run_pylint
                        exit 0
                        ;;
        --)             shift
                        ;;
    esac
fi

run_pep8_check

#if [ "${QUICK}" != 'true' ]
#then
#    run_pylint
#fi

if [ "${FAST}" == 'true' ]
then
    run_test_with_coverage -m 'not single_threaded' $(get_parallel_run_options) "$@"
elif [ "${QUICK}" == 'true' ]
then
    run_test_with_coverage -m 'not single_threaded and not rights_test' $(get_parallel_run_options) "$@"
else
    run_test_with_coverage "$@"
fi

echo -e "\nAll done"
exit 0
