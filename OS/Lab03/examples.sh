for file in *; do
    if [ -f "$file" ] && [ "$file" != "$(basename "$0")" ]; then
        temp_file=$(mktemp)
        sed 's/^ex:/Example:/g; s/\.ex:/\.Example:/g' "$file" > "$temp_file"
        if ! cmp -s "$file" "$temp_file"; then
            mv "$temp_file" "$file"
            echo "Processed: $file"
            ((files_processed++))
        else
            rm "$temp_file"
        fi
    fi
done
