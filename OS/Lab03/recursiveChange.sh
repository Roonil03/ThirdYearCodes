rm a.text b.text c.text d.text
touch a.txt b.txt c.txt d.txt

find . -name "*.txt" -type f | while read file; do
    dir=$(dirname "$file")
    base=$(basename "$file" .txt)
    new_name="$dir/$base.text"   
    mv "$file" "$new_name"
    echo "Renamed: $file -> $new_name"
done