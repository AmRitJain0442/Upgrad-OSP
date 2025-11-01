#!/bin/bash

# Script to create empty __init__.py files in all subdirectories
# Usage: ./create_init_files.sh [directory_path]

# Show help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [directory_path]"
    echo "  directory_path: Path to directory (defaults to current directory)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Current directory"
    echo "  $0 /path/to/project   # Specific directory"
    exit 0
fi

# Set target directory
TARGET_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Get absolute path and ask for permission
ABSOLUTE_PATH=$(cd "$TARGET_DIR" && pwd)
echo "This script will create empty __init__.py files in:"
echo "  $ABSOLUTE_PATH"
echo "  and all its subdirectories"
echo ""
echo "Do you want to proceed? (y/N)"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Create __init__.py files
created_count=0
skipped_count=0

while IFS= read -r -d '' dir; do
    init_file="$dir/__init__.py"
    
    if [ ! -f "$init_file" ]; then
        touch "$init_file"
        echo "Created: $init_file"
        ((created_count++))
    else
        echo "Skipped: $init_file (already exists)"
        ((skipped_count++))
    fi
done < <(find "$TARGET_DIR" -type d -print0)

echo ""
echo "Summary:"
echo "  Created: $created_count __init__.py files"
echo "  Skipped: $skipped_count existing __init__.py files"

if [ $created_count -gt 0 ]; then
    echo "Successfully created $created_count __init__.py files!"
else
    echo "No new __init__.py files were created."
fi