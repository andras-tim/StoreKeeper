#@IgnoreInspection AddShebangLine
### Main ###

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

EOF
}


# Init
cmd=
export GLOBAL_INSTALL=${GLOBAL_INSTALL:-false}
export PRODUCTION=${PRODUCTION:-false}
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
                                echo "Unknown parameter: $1" >&2
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
do_${cmd}
exit 0
