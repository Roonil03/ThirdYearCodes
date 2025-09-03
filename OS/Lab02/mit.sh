echo "Creating sample files with MIT content..."
cat > file1.txt << 'EOF'
This is about MIT research.
Students from MIT are brilliant.
MIT has great programs.
EOF

cat > file2.txt << 'EOF'
MIT technology is advanced.
The MIT campus is beautiful.
EOF

cat > file3.txt << 'EOF'
This file has no relevant content.
Just some random text here.
EOF

cat > document.txt << 'EOF'
MIT stands for Massachusetts Institute of Technology.
Many students aspire to join MIT.
MIT professors are world-renowned.
EOF

echo "1. Files containing 'MIT' in the current folder:"
echo "================================================"
grep -l "MIT" *.txt 2>/dev/null
echo ""
echo "2. Lines containing 'MIT' with replacement:"
echo "=========================================="
for file in $(grep -l "MIT" *.txt 2>/dev/null); do
    echo "File: $file"
    echo "----------"
    grep "MIT" "$file" | sed 's/MIT/Manipal Institute of Technology/g'
    echo ""
done
echo "4. Creating modified versions of files:"
echo "======================================"
for file in $(grep -l "MIT" *.txt 2>/dev/null); do
    output_file="${file%.txt}_modified.txt"
    sed 's/MIT/Manipal Institute of Technology/g' "$file" > "$output_file"
    echo "Created: $output_file"
done