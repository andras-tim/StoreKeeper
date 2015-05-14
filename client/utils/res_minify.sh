#!/bin/bash -e
cd "$(dirname "$0")/.."

function merge_resources()
{
    local path="$1"
    local extension="$2"
    local destination="$3"

    echo -n "${path}: "
    find "${path}" -name "*${extension}" -a \! -name "storekeeper*${extension}" | sort |
        while read path
        do
            echo -e "/*\n * @path: ${path}\n */"
            cat "${path}"
            echo -e "\n\n"
        done > "${destination}"
}

merge_resources app/js '.js' app/js/storekeeper.js
node_modules/minifier/index.js app/js/storekeeper.js --no-comments

merge_resources app/css '.css' app/css/storekeeper.css
node_modules/minifier/index.js app/css/storekeeper.css --no-comments

echo 'Done'
