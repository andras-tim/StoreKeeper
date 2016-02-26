#!/bin/bash -e
LF=$'\n'
TERMINAL_WIDTH=$(tput cols)
SESSION_NAME='sk'
CMD1='server/package.sh start'
CMD2='client/package.sh resources auto_prepare'
CMD3='docs/utils/doc_auto_rebuild.sh'
CMD4='server/utils/db_auto_migrate.sh'

tmux_base="tmux new-session -s ${SESSION_NAME}"
if [ "${TMUX}" != '' ]
then
    tmux_base='tmux new-window'
fi

server_pane_width=$[${TERMINAL_WIDTH} / 3]
if [ ${TERMINAL_WIDTH} -gt 110 -a ${server_pane_width} -lt 80 ]
then
    server_pane_width=80
fi

cd "$(dirname "$0")/.."
${tmux_base} \; \
    send-keys "${CMD1}${LF}" \; \
    split-window -p 80 \; \
    select-pane -U \; \
    split-window -h \; \
    send-keys "${CMD2}${LF}" \; \
    resize-pane -t 0 -x ${server_pane_width} \; \
    split-window -h \; \
    send-keys "${CMD3}${LF}" \; \
    split-window -h \; \
    send-keys "${CMD4}${LF}" \; \
    select-pane -D
