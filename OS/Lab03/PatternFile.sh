echo "Enter the folder path:"
read folder_path

echo "Enter the pattern to search for:"
read pattern

grep -l "$pattern" "$folder_path"/* 2>/dev/null | while read file; do
    basename "$file"
done

if [ $? -ne 0 ]; then
    echo "No files found containing the pattern '$pattern'."
fi