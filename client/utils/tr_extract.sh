#!/bin/bash -e
cd "$(dirname "$0")"
node_modules/grunt-cli/bin/grunt nggettext_extract
exit 0
