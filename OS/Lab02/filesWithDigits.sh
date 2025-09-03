for file in $(ls | grep '[0-9]'); do
    echo "File: $file"
    echo "Lines: $(wc -l < "$file")"
    echo "Words: $(wc -w < "$file")"
    echo "Characters: $(wc -c < "$file")"
    echo "Complete: $(wc "$file")"
    wc $file
    echo "---"
done
