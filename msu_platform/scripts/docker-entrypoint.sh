#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Function to wait for database
wait_for_db() {
    if [ "$DATABASE" = "postgres" ]; then
        echo "Waiting for postgres..."
        
        # Extract host and port from DATABASE_URL if needed, or use variables
        # For simplicity, we assume the DB host is 'db' as per docker-compose
        while ! nc -z $DB_HOST $DB_PORT; do
          sleep 0.1
        done

        echo "PostgreSQL started"
    fi
}

# wait_for_db # We'll use a more robust way if nc is available, or just rely on docker-compose healthchecks

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Execute the main command
echo "Starting server..."
exec "$@"
