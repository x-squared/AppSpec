from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_config
from .routers.registry import register_routers

app = FastAPI(title="AppSpec", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_config().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routers(app)


@app.get("/api/health")
def health_check():
    env = get_config().env.strip().upper()
    return {"status": "ok", "env": env, "dev_tools_enabled": env in {"DEV", "TEST"}}
