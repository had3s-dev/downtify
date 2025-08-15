#!/bin/bash

# Railway startup script for Downtify
# This script properly handles the PORT environment variable

set -e

# Get the port from environment variable, default to 8000
PORT=${PORT:-8000}

echo "Starting Downtify on port $PORT"

# Start the application with uvicorn
exec uvicorn main:app --host 0.0.0.0 --port $PORT
