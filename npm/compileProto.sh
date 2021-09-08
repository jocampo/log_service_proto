#!/bin/bash

set -e

PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROTO_PATH=$PWD/../proto/src
PROTO_DIR="${PWD}/proto_out"

rm -f "${PWD}/proto-objects.js"
rm -f "${PWD}/proto-objects.d.ts"
rm -rf "${PROTO_DIR}"

mkdir "${PROTO_DIR}"
cp -R "${PROTO_PATH}/" "${PROTO_DIR}"

TOP_LEVEL_PROTOS=( $(find ${PROTO_DIR} -name "*.proto") )

# JavaScript
pbjs --path "${PROTO_DIR}" ${TOP_LEVEL_PROTOS[@]}

# TypeScript
# pbts --out "${PWD}/proto-objects.d.ts" "${PWD}/proto-objects.js"
