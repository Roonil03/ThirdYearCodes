#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <option> <filename>"
    echo "Options:"
    echo "  -linecount   : Count lines"
    echo "  -wordcount   : Count words" 
    echo "  -charcount   : Count characters"
    exit 1
fi
option="$1"
filename="$2"
if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi
case "$option" in
    -linecount)
        lines=$(wc -l < "$filename")
        echo "Number of lines in '$filename': $lines"
        ;;
    -wordcount)
        words=$(wc -w < "$filename")
        echo "Number of words in '$filename': $words"
        ;;
    -charcount)
        chars=$(wc -c < "$filename")
        echo "Number of characters in '$filename': $chars"
        ;;
    *)
        echo "Error: Invalid option '$option'"
        echo "Valid options: -linecount, -wordcount, -charcount"
        exit 1
        ;;
esac
