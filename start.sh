#!/bin/bash

# 1. Start Redis in the background
echo "Starting Redis..."
redis-server --daemonize yes

# 2. Start the Celery Worker in the background
echo "Starting Celery Worker..."
celery -A worker.celery_app.celery worker --loglevel=info &

# 3. Start the FastAPI Application
echo "Starting FastAPI on port 7860..."
uvicorn app.main:app --host 0.0.0.0 --port 7860