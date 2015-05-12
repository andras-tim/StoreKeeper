#!/bin/bash -e
USERNAME='admin'
PASSWORD='admin'
COOKIE_FILE='/tmp/test-cookie'
BASE_URL='http://localhost:8000/storekeeper/api'
BASE_CURL_OPTS=(-s --dump-header - -H 'Content-Type: application/json')

# Examples:
#   ./api.sh GET /session
#   ./api.sh POST /user -d '{"username": "test", "password": "test", "email": "test@foo.bar"}'

function run_curl()
{
    local request="$1"; shift
    local url_tail="$1"; shift

    out="$(curl "${BASE_CURL_OPTS[@]}" -X "${request}" "${BASE_URL}${url_tail}" "$@")"
    echo "${out}"

    if echo "${out}" | grep -q 'HTTP/1\.0 401 UNAUTHORIZED'
    then
        return 1
    fi
    return 0
}

function get_last_cookie()
{
    if [ -e "${COOKIE_FILE}" ]
    then
        cat "${COOKIE_FILE}"
        return 0
    fi
    return 1
}

function get_new_cookie()
{
    echo "Getting new session cookie..." >&2
    run_curl POST /session -d '{"username": "'"${USERNAME}"'", "password": "'"${PASSWORD}"'"}' |
        grep '^Set-Cookie' |
        sed 's>^Set-Cookie: >>' |
        tr -d '\r\n' |
        tee "${COOKIE_FILE}"
}

function get_cookie()
{
    if get_last_cookie
    then
        return
    fi
    get_new_cookie
}


###
#  MAIN
request="$1"; shift
url_tail="$1"; shift

cookie="$(get_cookie)"
if run_curl "${request}" "${url_tail}" -b "${cookie}" "$@"
then
    exit 0
fi

cookie="$(get_new_cookie)"
run_curl "${request}" "${url_tail}" -b "${cookie}" "$@"
