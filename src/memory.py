import json
from typing import Any, Dict, Optional
import redis
from .config import settings


class RedisMemory:
    def __init__(self, namespace: str = "agent_state"):
        self.r = redis.from_url(settings.redis_url)
        self.ns = namespace

    def _key(self, session_id: str) -> str:
        return f"{self.ns}:{session_id}"

    def load(self, session_id: str) -> Dict[str, Any]:
        raw = self.r.get(self._key(session_id))
        if not raw:
            return {}
        return json.loads(raw)

    def save(self, session_id: str, state: Dict[str, Any]) -> None:
        self.r.set(self._key(session_id), json.dumps(state))


memory = RedisMemory()
