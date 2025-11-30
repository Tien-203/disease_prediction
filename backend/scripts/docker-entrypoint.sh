#!/bin/bash
# Docker entrypoint script for backend
# Runs migrations and starts the FastAPI application

set -e

echo "Starting backend container..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
max_attempts=30
attempt=0

until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-disease_user}" 2>/dev/null || [ $attempt -ge $max_attempts ]; do
  attempt=$((attempt + 1))
  echo "PostgreSQL is unavailable - sleeping (attempt $attempt/$max_attempts)"
  sleep 2
done

if [ $attempt -ge $max_attempts ]; then
  echo "PostgreSQL did not become ready in time. Exiting."
  exit 1
fi

echo "PostgreSQL is ready!"

# Run migration check script
echo "Checking database migrations..."
uv run python scripts/check_migrations.py

if [ $? -ne 0 ]; then
  echo "Migration check failed. Exiting."
  exit 1
fi

echo "Migrations check completed successfully."

# Start the application
echo "Starting FastAPI application..."
exec "$@"

