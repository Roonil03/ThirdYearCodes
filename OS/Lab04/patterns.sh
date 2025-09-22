#!/bin/bash

display_menu() {
    echo "      PATTERN OPERATIONS MENU     "
    echo "a. Search patterns in input file"
    echo "b. Delete all occurrences of patterns"
    echo "c. Exit"
    echo -n "Enter your choice (a/b/c): "
}

search_patterns() {
    local input_file="$1"
    shift
    local patterns=("$@")    
    echo "Searching patterns in file '$input_file'..."    
    for pattern in "${patterns[@]}"; do
        echo "Results for pattern: '$pattern'"
        if grep -n "$pattern" "$input_file" 2>/dev/null; then
            echo
        else
            echo "No matches found for pattern '$pattern'"
            echo
        fi
    done
}

delete_patterns() {
    local input_file="$1"
    shift
    local patterns=("$@")
    cp "$input_file" "${input_file}.backup"
    echo "Backup created: ${input_file}.backup"    
    echo "Deleting patterns from file '$input_file'..."    
    for pattern in "${patterns[@]}"; do
        echo "Deleting pattern: '$pattern'"
        sed -i "/$pattern/d" "$input_file"        
        if [ $? -eq 0 ]; then
            echo "Pattern '$pattern' deleted successfully"
        else
            echo "Error deleting pattern '$pattern'"
        fi
    done    
    echo "All specified patterns have been processed."
    echo "Modified file: $input_file"
    echo "Original backup: ${input_file}.backup"
}

clear
echo "Pattern Operations Script"
patterns=("$@")
echo "Patterns to process: ${patterns[*]}"
echo -n "Enter the input file name: "
read input_file
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' does not exist or is not a regular file."
    exit 1
fi
if [ ! -r "$input_file" ]; then
    echo "Error: File '$input_file' is not readable."
    exit 1
fi
echo "Input file: $input_file"
echo
while true; do
    display_menu
    read choice    
    case "$choice" in
        [Aa])
            echo
            search_patterns "$input_file" "${patterns[@]}"
            echo
            echo "Press Enter to continue..."
            read
            clear
            ;;
        [Bb])
            echo
            echo "WARNING: This will modify the original file!"
            echo -n "Are you sure you want to proceed? (y/n): "
            read confirm            
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                delete_patterns "$input_file" "${patterns[@]}"
            else
                echo "Operation cancelled."
            fi
            echo
            echo "Press Enter to continue..."
            read
            clear
            ;;
        [Cc])
            echo
            echo "Exiting the script. Goodbye!"
            exit 0
            ;;
        *)
            echo
            echo "Invalid choice! Please select a, b, or c."
            echo "Press Enter to continue..."
            read
            clear
            ;;
    esac
done
