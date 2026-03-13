from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


DEFAULT_SUPPORT_EMAIL = "support@example.org"
SUPPORT_TICKET_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "config"


@lru_cache(maxsize=1)
def _load_support_ticket_config() -> dict[str, str]:
    if not SUPPORT_TICKET_CONFIG_PATH.exists():
        return {"support_email": DEFAULT_SUPPORT_EMAIL}
    try:
        data = json.loads(SUPPORT_TICKET_CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"support_email": DEFAULT_SUPPORT_EMAIL}
    support_email = str((data.get("support") or {}).get("email", "")).strip() or DEFAULT_SUPPORT_EMAIL
    return {"support_email": support_email}


def get_support_ticket_email() -> str:
    return _load_support_ticket_config()["support_email"]
