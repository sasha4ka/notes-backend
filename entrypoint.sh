#!/bin/bash

echo "Applying migrations..."
alembic upgrade head

echo "Starting the application..."
exec "$@"