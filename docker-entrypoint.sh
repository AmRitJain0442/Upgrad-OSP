#!/bin/bash
set -e

# Fix permissions for mounted volumes
# This ensures that the appuser can read/write to the uploads directory
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, fixing permissions..."

    # Create uploads directory if it doesn't exist
    mkdir -p /app/uploads /app/logs

    # Fix permissions for uploads directory
    if [ -d "/app/uploads" ]; then
        echo "Fixing permissions for uploads directory..."
        chmod -R 755 /app/uploads
        chown -R appuser:appuser /app/uploads
    fi

    # Fix permissions for logs directory
    if [ -d "/app/logs" ]; then
        echo "Fixing permissions for logs directory..."
        chmod -R 755 /app/logs
        chown -R appuser:appuser /app/logs
    fi

    # Execute command as appuser using gosu
    echo "Switching to appuser..."
    exec gosu appuser "$@"
else
    # Already running as non-root user
    exec "$@"
fi
