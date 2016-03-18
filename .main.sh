### Main ###
set -e

function get_commands()
{
    declare -F | grep '^declare -f do_' | sed 's>^.*do_>>'
}

function get_code_of_init()
{
    if declare -F | grep -xq 'declare -f init'
    then
        local declaration="$(declare -f init)"
        # Drop first 3 and last lines
        echo "${declaration}" | tail -n +3 | head -n -1
    fi
}

function show_title()
{
    local dirname="$(basename "$(dirname "$0")")"
    local prefix=
    local args=

    if [ "${dirname}" != '.' ]; then
        prefix="${dirname}: "
    fi

    args="$(get_package_args)"
    if [ ! "${args}" == '' ]
    then
        args=" [${args}]"
    fi

    echo -e "\n### ${prefix}${cmd}${args} ###"
}

function get_package_args()
{
    local args=()

    if [ "${GLOBAL_INSTALL}" == true ]
    then
        args+=('global')
    fi

    if [ "${PRODUCTION}" == true ]
    then
        args+=('production')
    fi

    if [ "${FORCE}" == true ]
    then
        args+=('force')
    fi

    joined="$(printf ",%s" "${args[@]}")"
    echo "${joined:1}"
}

function show_help()
{
    cat - << EOF
$(basename "$0") [global-args] command [command-args]

Available commands:
$(get_commands | sort | sed 's>^>  * >')

Available global arguments:
  -h, --help            Show this help
  -g, --global          Install/make all changes on system
  -p, --production      Prepare environment for production use
  -f, --force           Do not ask anything

EOF
}

function run()
{
    "./$(basename "$0")" "$@"
}

function apt_get_install()
{
    local apt_args=
    if [ "${FORCE}" == true ]
    then
        apt_args='-y'
    fi

    sudo apt-get install ${apt_args} "$@"
}

function purge()
{
    local path="$1"

    if [ -e "${path}" ]
    then
        echo -n "Removing ${path}... "
        rm -r "${path}"
        echo 'Done'
    fi
}

function find_and_purge()
{
    find "$@" | while read rm_path
    do
        if [ -e "${rm_path}" ]
        then
            purge "${rm_path}"
        fi
    done
}

function make_default()
{
    local prefix="$1"
    local suffix="$2"

    if [ -e "${prefix}${suffix}" ]
    then
        return
    fi
    echo -n "Making default ${prefix}${suffix}... "
    cp -p "${prefix}.default${suffix}" "${prefix}${suffix}"
    echo "Done"
}


# Init
cmd=
args=
after_separator=false
export GLOBAL_INSTALL=${GLOBAL_INSTALL:-false}
export PRODUCTION=${PRODUCTION:-false}
export FORCE=${FORCE:-false}
while [ $# -gt 0 ]
do
    if [ "${cmd}" != '' ]
    then
        args="${args} $*"
        break
    fi

    case "$1" in
        --help|-h)          show_help
                            exit 0
                            ;;
        --global|-g)        export GLOBAL_INSTALL=true
                            ;;
        --production|-p)    export PRODUCTION=true
                            ;;
        --force|-f)         export FORCE=true
                            ;;
        *)                  if get_commands | grep -qx -- "$1"
                            then
                                cmd="$1"
                            else
                                echo "Unknown command: $1" >&2
                                exit 1
                            fi
                            ;;
    esac
    shift
done
if [ "${cmd}" == '' ]
then
    echo "Missing command parameter!" >&2
    show_help
    exit 1
fi


# Start
eval "$(get_code_of_init)"
show_title
do_${cmd} ${args}
exit 0
