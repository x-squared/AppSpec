from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _parse_list(value: str | None, default: list[str]) -> list[str]:
    if value is None:
        return default
    parts = [item.strip() for item in value.split(",")]
    return [item for item in parts if item]


@dataclass(frozen=True)
class AppConfig:
    env: str
    database_url: str
    cors_origins: list[str]


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    default_db_path = (Path(__file__).resolve().parents[2] / "database" / "tpl_app.db").as_posix()
    return AppConfig(
        env=os.getenv("TPL_ENV", "DEV"),
        database_url=os.getenv("TPL_DATABASE_URL", f"sqlite:///{default_db_path}"),
        cors_origins=_parse_list(os.getenv("TPL_CORS_ORIGINS"), ["http://localhost:5173"]),
    )
