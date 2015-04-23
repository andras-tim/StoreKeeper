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
        declaration="$(declare -f init)"
        # Drop first 3 and last lines
        echo "${declaration}" | tail -n +3 | head -n -1
    fi
}

function show_title()
{
    dirname="$(basename "$(dirname "$0")")"
    prefix=
    if [ "${dirname}" != '.' ]; then
        prefix="${dirname}: "
    fi
    echo -e "\n### ${prefix}${cmd} ###"
}

function show_help()
{
    cat - << EOF
$(basename "$0") command [arg]

Available commands:
$(get_commands | sort | sed 's>^>  * >')

Available arguments:
  -h, --help            Show this help
  -g, --global          Install/make all changes on system
  -p, --production      Prepare environment for production use
  -f, --force           Do not ask anything

EOF
}

function apt_get_install()
{
    args=
    if [ "${FORCE}" == true ]
    then
        args='-y'
    fi

    sudo apt-get install ${args} "$@"
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
    find . "$@" | while read rm_path
    do
        if [ -e "${rm_path}" ]
        then
            purge "${rm_path}"
        fi
    done
}

# Init
cmd=
args=
export GLOBAL_INSTALL=${GLOBAL_INSTALL:-false}
export PRODUCTION=${PRODUCTION:-false}
export FORCE=${FORCE:-false}
while [ $# -gt 0 ]
do
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
        *)                  if [ "${cmd}" == '' ]
                            then
                                if get_commands | grep -qx -- "$1"
                                then
                                    cmd="$1"
                                else
                                    echo "Unknown command: $1" >&2
                                    exit 1
                                fi
                            else
                                args="${args} $1"
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
