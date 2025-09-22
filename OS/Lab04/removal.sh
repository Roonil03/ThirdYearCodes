#!/bin/bash

for file in "$@"; do
    if [ -f "$file" ]; then
        echo -n "Do you want to remove '$file'? (y/n): "
        read response
        case "$response" in
            [Yy]|[Yy][Ee][Ss])
                rm "$file"
                if [ $? -eq 0 ]; then
                    echo "File '$file' removed successfully."
                else
                    echo "Error: Failed to remove '$file'"
                fi
                ;;
            *)
                echo "File '$file' not removed."
                ;;
        esac
    else
        echo "Warning: File '$file' does not exist."
    fi
done
