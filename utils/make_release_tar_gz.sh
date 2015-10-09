#!/bin/bash -e

CURRENT_DIR="$(pwd)"
TEMPDIR="$(mktemp -d -t 'sk-XXXXXX')"
cd "${TEMPDIR}"

git clone 'https://github.com/andras-tim/StoreKeeper.git'
cd StoreKeeper

mkdir -p "$(pwd)/server/tmp/pip-download-cache"
./package.sh -p install

echo -e '\nCleaning up...'
rm -rf .git
rm -rf server/flask

VERSION="$(grep '"version"' client/package.json | sed -E 's>.*"version".*"(.*)".*>\1>')"
DESTINATION_FILE="${CURRENT_DIR}/StoreKeeper-v${VERSION}.tar.gz"
echo -e "\nCreating release... ${DESTINATION_FILE}"
cd "${TEMPDIR}"
tar czf "${DESTINATION_FILE}" StoreKeeper

cd "${CURRENT_DIR}"
rm -rf "${TEMPDIR}"
echo 'Done'
