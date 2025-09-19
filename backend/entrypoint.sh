#!/usr/bin/env bash
set -euo pipefail

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
