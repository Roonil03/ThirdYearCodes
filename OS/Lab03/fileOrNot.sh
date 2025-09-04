#!/bin/bash
echo "Enter the file/directory path:"
read filepath

if [ ! -e "$filepath" ]; then
    echo "Error: '$filepath' does not exist."
    exit 1
elif [ -d "$filepath" ]; then
    echo "'$filepath' is a directory."
elif [ -f "$filepath" ]; then
    echo "'$filepath' is a regular file."
# else
#     echo "'$filepath' is neither a regular file nor a directory (possibly a special file)."
fi
