#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for MySQL to start..."
python << END
import sys
import time
import MySQLdb

for _ in range(30):  # Try for 30 seconds
    try:
        MySQLdb.connect(
            host="${DATABASE_HOST}",
            user="${DATABASE_USER}",
            passwd="${DATABASE_PASSWORD}",
            db="${DATABASE_NAME}"
        )
        print("Database connection successful!")
        sys.exit(0)
    except MySQLdb.OperationalError:
        print("Database not ready yet, waiting...")
        time.sleep(1)

print("Could not connect to database after 30 seconds")
sys.exit(1)
END

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
exec "$@"