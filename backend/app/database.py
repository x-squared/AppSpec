from pathlib import Path
from urllib.parse import unquote, urlparse

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_config

cfg = get_config()

if cfg.database_url.startswith("sqlite:///"):
    raw_path = unquote(cfg.database_url[len("sqlite:///") :])
    if raw_path and raw_path != ":memory:":
        db_path = Path(raw_path)
        if not db_path.is_absolute():
            db_path = (Path.cwd() / db_path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if cfg.database_url.startswith("sqlite") else {}
engine = create_engine(cfg.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    row_version = Column("ROW_VERSION", Integer, nullable=False, default=1)
    @property
    def changed_at(self):
        """Compatibility alias for legacy updated_at field during phased rename."""
        return getattr(self, "updated_at", None)

    @changed_at.setter
    def changed_at(self, value):
        if hasattr(self, "updated_at"):
            setattr(self, "updated_at", value)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
