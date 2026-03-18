import redis
import hashlib
from app.core.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def get_cache_key(text: str):
    return hashlib.sha256(text.encode()).hexdigest()

def get_cached(text: str):
    return r.get(get_cache_key(text))

def set_cache(text: str, summary: str):
    r.set(get_cache_key(text), summary)