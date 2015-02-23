#!/bin/bash -e
BASEDIR="$(dirname "$0")"
HTML_REPORT_PATH="${BASEDIR}/tmp/coverage"

function coverage()
{
    local command="$1"; shift

    "${BASEDIR}/flask/bin/coverage" "${command}" --rcfile "${BASEDIR}/.coveragerc" "$@"
}


mkdir -p "${HTML_REPORT_PATH}"

coverage run "${BASEDIR}/test.py"

echo -e "\n\nCoverage Report:\n"
coverage report -m

echo -e "\nHTML version: ${HTML_REPORT_PATH}/index.html"
coverage html -d "${HTML_REPORT_PATH}"
