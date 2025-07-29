#!/bin/sh
set -e

echo "Waiting for Postgres..."
until pg_isready -h $POSTGRES_HOST -d $POSTGRES_DB -U $POSTGRES_USER; do
  sleep 5
done

echo "Postgres is up. Running migrations..."
alembic upgrade head

echo "Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port 8002