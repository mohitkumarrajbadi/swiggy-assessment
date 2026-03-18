import os
from dotenv import load_dotenv

load_dotenv()

# We offload Postgres to an external provider like Neon.tech for persistence.
DATABASE_URL = os.getenv("DATABASE_URL")

# These default to the internal services started by our start.sh script.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Hugging Face Inference API configuration
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "facebook/bart-large-cnn")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")