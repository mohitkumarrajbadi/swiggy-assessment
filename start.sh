#!/bin/bash

# 1. Start the Celery Worker in the background
# We limit concurrency to 1 to stay within Railway's 512MB RAM limit
echo "Starting Celery Worker..."
celery -A worker.celery_app.celery worker --loglevel=info --concurrency=1 &

# 2. Start the FastAPI Application
# Railway provides the PORT environment variable
echo "Starting FastAPI on port ${PORT:-7860}..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}