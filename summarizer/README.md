# AI Summarizer Service

An asynchronous, distributed AI service built to summarize articles, documents, or long text quickly using self-hosted LLMs.

## Overview

Summarizing long text using LLMs can take several seconds. This service uses a decoupled architecture to accept user requests instantly, process them in the background via Celery, and store results for later retrieval. It includes a built-in Redis caching layer to provide sub-millisecond responses for previously summarized content.

## Architecture

- **FastAPI**: High-performance web framework for the API layer.
- **Celery**: Distributed task queue for asynchronous processing.
- **Redis**: Acts as both the Celery message broker and the result cache.
- **PostgreSQL**: Persistent storage for job status, results, and processing metrics.
- **Ollama**: Local LLM engine (Llama2) used for inference.

[View Full Architecture Documentation (High/Low Level Design)](file:///Users/mohitbadi/.gemini/antigravity/brain/de7ec6f8-8d4e-4acb-93d6-f3549b3bedbd/architecture.md)

## Project Structure

| File / Directory | Description |
| :--- | :--- |
| `app/api/routes.py` | API endpoints and request hashing for idempotency. |
| `app/services/fetcher.py` | Metadata-aware web extraction (supports React/SPA). |
| `app/services/summarizer.py` | Persona-driven LLM prompt engineering for cleaner summaries. |
| `worker/tasks.py` | Background worker logic and performance tracking. |
| `app/core/database.py` | Resilient database connection pool with automatic retries. |
| `tests/` | Comprehensive unit and integration test suite. |

## Advanced Features & Edge Cases

- **Metadata-Aware Fetching (SPA Support)**: Modern sites (like Portfolios) often have empty bodies on first load. Our fetcher falls back to SEO Meta tags to ensure content is always captured.
- **System Analyst Persona**: The LLM is strictly instructed to ignore HTML code and focus on the human substance of the text.
- **Idempotency & Caching**: SHA-256 content hashing ensures that the same article is never summarized twice, saving computing power.
- **Startup Resilience**: The API automatically retries database connections, preventing crashes during multi-container Docker boots.

## Setup & Installation

### Prerequisites
- Docker & Docker Compose
- [Ollama](https://ollama.com/) installed and running locally

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd summarizer
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```

3. **Start the Services**:
   ```bash
   docker-compose up --build
   ```

4. **Prepare the LLM**:
   Ensure you have the required model pulled in Ollama:
   ```bash
   ollama pull llama2
   ```

## API Endpoints

### 1. Submit Content
**POST** `/submit`
- Body: `{"url": "https://example.com"}` OR `{"text": "Your long text..."}`
- Returns: `{"job_id": "uuid", "status": "queued"}`

### 2. Check Status
**GET** `/status/{job_id}`
- Returns: `{"job_id": "uuid", "status": "completed", "created_at": "timestamp"}`

### 3. Retrieve Result
**GET** `/result/{job_id}`
- Returns:
  ```json
  {
    "job_id": "uuid",
    "original_url": "https://example.com",
    "summary": "The generated summary...",
    "cached": false,
    "processing_time_ms": 8500
  }
  ```

## Testing

The project includes a comprehensive test suite (unit + integration).

**Run tests locally**:
```bash
DATABASE_URL=sqlite:///:memory: PYTHONPATH=. ./venv/bin/pytest tests/
```

## Edge Cases Handled
- **Idempotency**: Repeated submissions of the same content are served instantly from the Redis cache.
- **Robust Fetching**: Detailed error handling for invalid URLs and network timeouts.
- **Graceful Failure**: If the LLM or network fails, the job status is updated to `failed` with the error reason preserved.
- **Local Dev Stability**: Disabled SSL verification for local fetcher tests to avoid certificate issues in dev environments.
