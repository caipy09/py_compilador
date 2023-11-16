#!/bin/bash

# Some useful functions
show_usage() {
    echo "Usage: $0 -f [file_path] [-o [output_file]]"
    exit 1
}

# Exit with compilation error
exit_error() {
    echo -en "\n\033[31mCompilation error\033[0m\n"
    exit 1
}

get_name() {
    local filename=$(basename "$1")
    local name="${filename%.*}"

    # Check if the file name is the same as its extension
    if [[ "$filename" == "$name" ]] || [[ "$filename" == .* ]]; then
        echo "$filename"
    else
        echo "$name"
    fi
}

# Initialize variables
file_path=""
TMP_PATH="/tmp"
BUILD_PATH="build"
# Parse command-line options
while getopts 'f:o:' flag; do
    case "${flag}" in
        f) file_path="${OPTARG}" ;;
        o) output_file="${OPTARG}" ;;
        *) show_usage ;;
    esac
done


# Check if file path was provided
if [ -z "$file_path" ]; then
    echo "Error: File path not provided."
    show_usage
fi

if [[ ! -d ".venv" ]]; then
    virtualenv --download --always-copy -p /usr/bin/python3.8 .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi;

source .venv/bin/activate

if [[ ! -d $BUILD_PATH ]]; then
    mkdir $BUILD_PATH
fi;


python3 transpiler.py $file_path
if [[ $? != 0 ]]; then
    echo "Error assembling file $file_path"
    exit_error
fi

file_basename=$(basename $file_path)
name=$(get_name $file_basename)

# Output file is optional
if [ -z "$output_file" ]; then
    echo "Note: Output file not specified. output file will be ./$BUILD_PATH/$name"
    output_file=$(pwd)/$BUILD_PATH/$name
else
    echo "Compiled executable: $output_file"
fi

nasm -f elf64 -g -F dwarf ./lib/libitoa.asm -o ./lib/libitoa.o
if [[ $? != 0 ]]; then
    echo "compiling libitoa failed"
    exit_error
fi

nasm -f elf64 -g -F dwarf ./lib/libprint.asm -o ./lib/libprint.o
if [[ $? != 0 ]]; then
    echo "compiling libprint failed"
    exit_error
fi

# Compila el archivo main
nasm -f elf64 -g -F dwarf "$TMP_PATH/$name.asm" -o "$TMP_PATH/$name.o"
if [[ $? != 0 ]]; then
    echo "compiling $TMP_PATH/$name.asm failed"
    exit_error
fi

# Enlaza los objetos en un ejecutable
ld "$TMP_PATH/$name.o" ./lib/libitoa.o ./lib/libprint.o -o "$output_file" -g
if [[ $? != 0 ]]; then
    echo "Failed linking $TMP_PATH/$name.o"
    exit_error
fi

rm "$TMP_PATH/$name.o"
chmod +x "$output_file"
if [[ $? != 0 ]]; then
    echo "Error setting execution permission to $output_file. But"
fi

echo -e "\e[1;32m'$output_file' compiled successfully!\n\e[0m"

exit 0 
