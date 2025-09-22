#!/usr/bin/env bash
read -r -p "Enter file name: " file
[[ ! -e $file ]] && { echo "File not found"; exit 1; }
perm=$(stat -c %A "$file")
owner=${perm:1:3}
group=${perm:4:3}
other=${perm:7:3}
echo "Permissions for $file"
echo "  Owner : $owner"
echo "  Group : $group"
echo "  Other : $other"
