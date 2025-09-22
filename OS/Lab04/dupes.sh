#!/bin/bash

filename="$1"
if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi
duplicate_name="${filename%.*}_copy.${filename##*.}"
if [ "$filename" = "${filename%.*}" ]; then
    duplicate_name="${filename}_copy"
fi
cp "$filename" "$duplicate_name"
