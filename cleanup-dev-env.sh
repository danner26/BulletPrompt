#!/bin/bash

# Array of files and folders to remove
items_to_remove=(
    "BulletPrompt.egg-info"
    "build"
    "bullet.egg-info"
    "dist"
)

# Loop through the array and remove each item
for item in "${items_to_remove[@]}"; do
    if [ -e "$item" ]; then
        rm -rf "$item"
        echo "Removed $item"
    fi
done
