#!/bin/bash

replace_slash() {
    local path="$1"
    echo "${path//\//_}"
}
find tests/ \
    -type f \
    -name "input.txt" \
    -exec bash -c 'echo -en "\nCompilando archivo $1\n"; path="$1"; source ./.venv/bin/activate; ./compile.sh -f $1 -o ./build/${path//\//_}' _ {} \;
