#!/bin/bash

# A more realistic sample script
echo "Starting task..."
echo "Processing data for user: $TARGET_USER"

# Fetch data and redirect output to a file
curl "https://api.github.com/users/$TARGET_USER" > /tmp/user_data.json

echo "User data saved to /tmp/user_data.json"

# List the contents of the tmp directory
ls -l /tmp

# Clean up the created file
rm /tmp/user_data.json

echo "Task finished."