from __future__ import annotations

from contextvars import ContextVar

_current_changed_by_id: ContextVar[int | None] = ContextVar("current_changed_by_id", default=None)


def set_current_changed_by_id(user_id: int | None) -> None:
    _current_changed_by_id.set(user_id)


def get_current_changed_by_id() -> int | None:
    return _current_changed_by_id.get()


def clear_current_changed_by_id() -> None:
    _current_changed_by_id.set(None)
