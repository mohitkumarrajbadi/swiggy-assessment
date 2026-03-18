import os
from dotenv import load_dotenv

load_dotenv()

# We offload Postgres to an external provider like Neon.tech for persistence.
DATABASE_URL = os.getenv("DATABASE_URL")

# These default to the internal services started by our start.sh script.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Hugging Face Inference API configuration
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "facebook/bart-large-cnn")