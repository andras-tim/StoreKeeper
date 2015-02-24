#!/bin/bash -e
function show_git_config()
{
    cat - <<EOF

------8<------------------------------------------------------------------------------------------------------->8-------

Please, verify your git user for future contribution ;)
  Uername: '$(git config user.name)'
  Email:   '$(git config user.email)'

EOF
}

function do_install()
{
    server/package.sh preinstall
    server/package.sh postinstall

    docs/package.sh install

    echo -e "\nAll Done!"
    show_git_config
}

function do_start()
{
    server/package.sh start
}

function do_clear()
{
    server/package.sh clear

    doc/package.sh clear
}


cd "$(dirname "$0")"
source .main.sh
