#!/bin/bash -e
SCRIPTS=('client/utils/res_auto_minify.sh' 'client/utils/tr_auto_compile.sh' 'docs/utils/doc_auto_rebuild.sh')
PIDS=()
cd "$(dirname "$0")/.."


function terminate_scripts()
{
    echo
    for pid in "${PIDS[@]}"
    do
        echo "Terminating pid ${pid}"
        kill "${pid}"
    done
    exit 130
}


trap terminate_scripts INT

for script in "${SCRIPTS[@]}"
do
    echo -n "Starting ${script}... "
    "${script}" &
    PIDS+=($!)
    echo "pid $!"
done

for pid in "${PIDS[@]}"
do
    wait ${pid}
    echo Terminated "pid ${pid}"
done

exit 0
