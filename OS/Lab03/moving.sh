echo "Enter file extension (without dot, e.g., txt):"
read extension

echo "Enter destination folder name:"
read dest_folder

if [ ! -d "$dest_folder" ]; then
    mkdir -p "$dest_folder"
    echo "Created folder: $dest_folder"
fi

count=0

for file in *."$extension"; do
    if [ -f "$file" ]; then
        cp "$file" "$dest_folder/"
        echo "Copied: $file -> $dest_folder/"
        ((count++))
    fi
done
