#!/bin/bash

# Ensure local bin is in path
export PATH=$PATH:/home/user/.local/bin

# 1. Start Redis in the background
echo "Starting Redis..."
redis-server --daemonize yes

# 2. Start Ollama in the background
echo "Starting Ollama..."
ollama serve &
sleep 5

# 3. Pull the model
echo "Pulling Llama2 model..."
ollama pull llama2

# 4. Start the Celery Worker
echo "Starting Celery Worker..."
celery -A worker.tasks.celery worker --loglevel=info &

# 5. Start the FastAPI Application on the required HF port
echo "Starting FastAPI on port 7860..."
uvicorn app.main:app --host 0.0.0.0 --port 7860
