from fastapi import FastAPI

from . import dev_forum, support_ticket


def register_routers(app: FastAPI) -> None:
    """Register routers that are currently present in AppSpec."""
    app.include_router(dev_forum.router, prefix="/api")
    app.include_router(support_ticket.router, prefix="/api")
