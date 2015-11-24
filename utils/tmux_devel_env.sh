#!/bin/bash -e
LF=$'\n'
SESSION_NAME='sk'
CMD1='server/package.sh start'
CMD2='client/package.sh resources auto_prepare'
CMD3='docs/utils/doc_auto_rebuild.sh'

tmux_base="tmux new-session -s ${SESSION_NAME}"
if [ "${TMUX}" != '' ]
then
    tmux_base='tmux new-window'
fi

cd "$(dirname "$0")/.."
${tmux_base} \; \
    send-keys "${CMD1}${LF}" \; \
    split-window -p 80 \; \
    select-pane -U \; \
    split-window -h \; \
    send-keys "${CMD2}${LF}" \; \
    resize-pane -t 0 -x 80 \; \
    split-window -h \; \
    send-keys "${CMD3}${LF}" \; \
    select-pane -D
