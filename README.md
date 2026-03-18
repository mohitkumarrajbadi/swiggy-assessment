# 🚀 AI Summarizer Service

An **asynchronous, distributed backend service** that summarizes web content and long-form text using modern LLM APIs. Built with a focus on scalability, reliability, and real-world production constraints.

---

## 🌐 Live Demo

You can test the API and explore live documentation here:
👉 **[Swagger UI (Live API)](https://swiggy-assessment-production.up.railway.app/docs)**

---

## 🧠 Why This Exists?

Summarizing large articles using LLMs can be slow (several seconds per request). To ensure a smooth user experience, this system uses a **decoupled architecture**:

1.  **Instant Acceptance**: Submit a URL and get a `job_id` back in milliseconds.
2.  **Async Processing**: High-latency LLM calls happen in the background via Celery.
3.  **Smart Caching**: Repeated requests for the same content are served instantly from Redis.

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client[Client] --> API[FastAPI]
    API --> Redis[Redis Queue]
    Redis --> Worker[Celery Worker]
    Worker --> LLM[Hugging Face Router API]
    Worker --> DB[(PostgreSQL)]
    DB --> API
    API --> Cache[Redis Cache]
```

### Technical Stack
- **Framework**: FastAPI (High-performance Python)
- **Task Queue**: Celery + Redis
- **Persistence**: PostgreSQL (SQLAlchemy)
- **AI Engine**: Hugging Face AI Router (`Mistral-7B` / `GPT-OSS`)
- **Deployment**: Railway (Cloud Native)

---

## ✨ Key Features

- **⚡ Non-Blocking API**: Distributed task execution ensures the main thread stays responsive.
- **🌐 SPA-Aware Scraping**: Handles modern JavaScript-heavy websites (React/Vue portfolios).
- **🧠 Prompt Engineering**: Specialized prompts filter out HTML noise and focus on semantic insights.
- **🔁 Idempotency**: Content hashing prevents redundant LLM calls for the same input.
- **🛡️ Fault Tolerance**: Built-in retry logic and robust error tracking for every job.

---

## 📁 Project Structure

| Path | Description |
|------|------------|
| `app/api/routes.py` | REST endpoints and request orchestration |
| `app/services/fetcher.py` | Web content extraction with SEO fallback |
| `app/services/summarizer.py` | LLM integration and prompt logic |
| `worker/tasks.py` | Asynchronous job execution logic |
| `app/core/database.py` | Database connection and session management |

---

## ⚙️ Local Development

### Prerequisites
- Python 3.10+
- Redis Server
- PostgreSQL Instance
- Hugging Face API Key

### 1. Installation
```bash
git clone <your-repo-url>
cd swiggy-assessment
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file (see `.env.example`):
```env
HF_API_KEY=your_huggingface_token
DATABASE_URL=postgresql://user:password@localhost/db
REDIS_URL=redis://localhost:6379/0
```

### 3. Run Services
```bash
# Start the API
uvicorn app.main:app --reload

# Start the Worker (in a separate terminal)
celery -A worker.celery_app worker --loglevel=info --concurrency=1
```

---

## 📡 API Usage

### 1. Submit a Job
**POST** `/submit`
```json
{
  "url": "https://example.com/article"
}
```

### 2. Check Result
**GET** `/result/{job_id}`
```json
{
  "job_id": "uuid",
  "status": "completed",
  "summary": "This article discusses...",
  "processing_time_ms": 1200
}
```

---

## 🔥 Production Evolution (Interviewer Highlights)

During the development of this assessment, the following high-level SDE decisions were made:
- **Ollama → HF API**: Moved from local containerized LLMs to a serverless API Router to optimize for memory constraints (512MB RAM).
- **Decoupled Workers**: Implemented a dedicated Celery worker to separate CPU-intensive scraping and API calls from the IO-bound FastAPI web server.
- **Unified Caching**: Integrated a Redis-based caching layer that yields sub-50ms response times for repeat queries.

---

## 👨‍💻 Author
**Mohit Kumar Raj Badi**
AI & Backend Engineer