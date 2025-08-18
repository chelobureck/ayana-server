import httpx
import orjson
from .config import settings
from .cache import get_cached_completion, set_cached_completion
from .prompts import SYSTEM_ORCHESTRATOR, ROLE_AYYA, ROLE_AYANA, CORRECTION_INSTRUCTIONS, PROJECT_GUIDE

HEADERS = {
    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

async def chat_completion(messages: list[dict]) -> dict:
    # cache first
    cached = get_cached_completion(messages)
    if cached:
        return orjson.loads(cached)

    payload = {
        "model": settings.OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }
    async with httpx.AsyncClient(base_url=settings.OPENAI_BASE_URL, timeout=settings.OPENAI_TIMEOUT) as client:
        r = await client.post("/chat/completions", headers=HEADERS, content=orjson.dumps(payload))
        r.raise_for_status()
        data = r.json()
    choice = data["choices"][0]["message"]["content"]
    set_cached_completion(messages, choice)
    return orjson.loads(choice)

async def orchestrate_turn(dialog: list[dict]) -> dict:
    system = {
        "role": "system",
        "content": (
            SYSTEM_ORCHESTRATOR + "\n" + ROLE_AYYA + "\n" + ROLE_AYANA + "\n" + CORRECTION_INSTRUCTIONS + "\n" + PROJECT_GUIDE
        ),
    }
    messages = [system] + dialog
    return await chat_completion(messages) 