#!/usr/bin/env bash
set -e  # fail on error

echo "Running database migrations..."
flyway migrate

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000