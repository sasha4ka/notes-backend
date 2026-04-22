#!/bin/sh

echo "Waiting for the database to be ready..."
python wait_for_db.py

echo "Applying migrations..."
alembic upgrade head

echo "Starting the application..."
exec "$@"