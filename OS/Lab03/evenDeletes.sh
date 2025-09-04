echo "Enter the path to the text file:"
read filepath

total_lines=$(wc -l < "$filepath")
echo "Original file has $total_lines lines."

temp_file=$(mktemp)

sed '2~2d' "$filepath" > "$temp_file"

mv "$temp_file" "$filepath"

remaining_lines=$(wc -l < "$filepath")
deleted_lines=$((total_lines - remaining_lines))

echo "Deleted $deleted_lines even-numbered lines."