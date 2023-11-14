#!/bin/bash

# Some useful functions
show_usage() {
    echo "Usage: $0 -f [file_path] [-o [output_file]]"
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



python3 transpiler.py $file_path

file_basename=$(basename $file_path)
name=$(get_name $file_basename)

# Output file is optional
if [ -z "$output_file" ]; then
    echo "Note: Output file not specified. output file will be ./$name"
    output_file=$(pwd)/$name
else
    echo "Compiled executable: $output_file"
fi







nasm -f elf64 -g -F dwarf ./lib/libitoa.asm -o ./lib/libitoa.o
nasm -f elf64 -g -F dwarf ./lib/libprint.asm -o ./lib/libprint.o

# Compila el archivo main
nasm -f elf64 -g -F dwarf $TMP_PATH/$name.asm -o $TMP_PATH/$name.o

# Enlaza los objetos en un ejecutable
ld $TMP_PATH/$name.o ./lib/libitoa.o ./lib/libprint.o -o $output_file -g
rm $TMP_PATH/$name.o
chmod +x $output_file
echo -e "\e[1;32m'$output_file' compiled successfully!\n\e[0m"

exit 0
