import hashlib
import json
import redis
from .config import settings

_redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def _hash_messages(messages: list[dict]) -> str:
    key = json.dumps(messages, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def get_cached_completion(messages: list[dict]) -> str | None:
    digest = _hash_messages(messages)
    return _redis.get(f"llm:{digest}")

def set_cached_completion(messages: list[dict], value: str):
    digest = _hash_messages(messages)
    _redis.setex(f"llm:{digest}", settings.REDIS_TTL_SECONDS, value) 