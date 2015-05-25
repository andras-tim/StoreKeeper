#!/bin/bash -e
cd "$(dirname "$0")/.."
node_modules/grunt-cli/bin/grunt nggettext_compile
sed "1i'use strict';\n" -i app/js/src/translations.js
exit 0
